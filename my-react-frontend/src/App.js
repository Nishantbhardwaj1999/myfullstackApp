import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Typography, Container } from '@mui/material';

function App() {
  const [item, setItem] = useState('');
  const [itemId, setItemId] = useState('');
  const [message, setMessage] = useState('');

  const handleCreateItem = async () => {
    try {
      const response = await axios.post('http://localhost:5000/items', { item });
      setMessage(response.data);
    } catch (error) {
      setMessage('Failed to create item');
    }
  };

  const handleGetItem = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/items/${itemId}`);
      setMessage(JSON.stringify(response.data));
    } catch (error) {
      setMessage('Item not found');
    }
  };

  const handleUpdateItem = async () => {
    try {
      const response = await axios.put(`http://localhost:5000/items/${itemId}`, { item: item, itemId: itemId });
      setMessage(response.data);
    } catch (error) {
      setMessage('Failed to update item');
    }
  };
  

  const handleDeleteItemKey = async (key) => {
    try {
      const response = await axios.delete(`http://localhost:5000/items/${itemId}/${key}`);
      setMessage(response.data);
    } catch (error) {
      setMessage('Failed to delete key');
    }
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h3" gutterBottom>Flask Backend with React Frontend</Typography>
      <div>
        <TextField 
          label="Item" 
          variant="outlined" 
          value={item} 
          onChange={(e) => setItem(e.target.value)} 
          fullWidth 
          margin="normal" 
        />
        <Button variant="contained" onClick={handleCreateItem}>Create Item</Button>
      </div>
      <div>
        <TextField 
          label="Item ID" 
          variant="outlined" 
          value={itemId} 
          onChange={(e) => setItemId(e.target.value)} 
          fullWidth 
          margin="normal" 
        />
        <Button variant="contained" onClick={handleGetItem}>Get Item</Button>
      </div>
      <div>
        <Button variant="contained" onClick={handleUpdateItem}>Update Item</Button>
      </div>
      <div>
        <Button variant="contained" onClick={() => handleDeleteItemKey('key_name')}>Delete Key</Button>
      </div>
      <div>
        <Typography variant="h6">Message: {message}</Typography>
      </div>
    </Container>
  );
}

export default App;
