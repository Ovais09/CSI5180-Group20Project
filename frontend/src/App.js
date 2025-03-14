import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
function App() {
  const [userInput, setUserInput] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(userInput);
    const response = await fetch('http://127.0.0.1:5000/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input: userInput })
    });
    const data = await response.json();
    console.log("Response from backend:", data);
    setResult(data.result);
  };

  return (
    <div>
      <h1>Python Execution Example</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          placeholder="Enter something"
        />
        <button type="submit">Submit</button>
      </form>
      <p>Result: {result}</p>
    </div>
  );
}

export default App;