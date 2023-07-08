// Fetch trading bot output and update the output element
function fetchBotOutput() {
    // Replace this with your code to fetch the trading bot's output
    const botOutput = 'SELL: AAPL at 150.5\nBUY: AAPL at 145.3\nNo trade';
  
    const outputElement = document.getElementById('output');
    outputElement.textContent = botOutput;
  }
  
  // Call the fetchBotOutput function when the page is loaded
  window.addEventListener('load', fetchBotOutput);
  