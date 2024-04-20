import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Load data
df = pd.read_csv('4.17.2024tsv.tsv', delimiter='\t', header=None, names=['index', 'post_title', 'target_paragraphs', 'spoiler'])

# Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Custom Dataset
class SpoilerDataset(Dataset):
    def __init__(self, dataframe, tokenizer):
        self.data = dataframe
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        post_title = str(row['post_title'])
        target_paragraphs = str(row['target_paragraphs'])
        spoiler = str(row['spoiler'])
        inputs = self.tokenizer.encode_plus(
            post_title,
            target_paragraphs,
            add_special_tokens=True,
            max_length=512,
            truncation_strategy='longest_first',
            padding='max_length',
            return_tensors='pt'
        )
        return {
            'input_ids': inputs['input_ids'].flatten(),
            'attention_mask': inputs['attention_mask'].flatten(),
            'labels': torch.tensor(int(spoiler))
        }

# Split data
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)

# Datasets and DataLoaders
train_dataset = SpoilerDataset(train_df, tokenizer)
train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True)

val_dataset = SpoilerDataset(val_df, tokenizer)
val_dataloader = DataLoader(val_dataset, batch_size=4, shuffle=False)

# Model
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Optimizer
optimizer = AdamW(model.parameters(), lr=5e-5)

# Training Loop
num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    for batch in tqdm(train_dataloader, desc=f'Epoch {epoch+1}', leave=False):
        optimizer.zero_grad()
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        loss.backward()
        optimizer.step()

    model.eval()
    val_loss = 0.0
    for batch in val_dataloader:
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['labels'].to(device)
        with torch.no_grad():
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            val_loss += outputs.loss.item()

    val_loss /= len(val_dataloader)
    print(f'Validation Loss: {val_loss:.4f}')

# Save the model
model.save_pretrained('your_model_directory')
