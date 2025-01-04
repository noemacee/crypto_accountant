import React, { useState } from "react";
import api from "../api";

const WalletProcessor = () => {
  const [apiKey, setApiKey] = useState("");
  const [walletAddress, setWalletAddress] = useState("");
  const [responseMessage, setResponseMessage] = useState("");
  const [csvPath, setCsvPath] = useState(null);
  const [error, setError] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(false); // Reset error state

    console.log("Form submitted"); // Log when the form is submitted
    console.log("API Key:", apiKey); // Log the API key
    console.log("Wallet Address:", walletAddress); // Log the wallet address


    if (!apiKey || !walletAddress) {
      setError(true);
      setResponseMessage("Both API key and wallet address are required!");
      return;
    }

    try {
      const response = await api.post(
        "/wallet/process_wallet",
        { wallet_address: walletAddress },
        { headers: { "X-API-Key": apiKey } }
      );


      if (response.data.csv_path) {
        setCsvPath(response.data.csv_path);
        setResponseMessage(response.data.message || "Wallet processed successfully.");
      } else {
        setResponseMessage("No CSV path received, but wallet processed successfully.");
      }
    } catch (error) {
      setError(true);
      setResponseMessage(
        error.response?.data?.error || "An error occurred. Please try again."
      );
    }
  };

  return (
    <div className="processor-container">
      <h1>Crypto Wallet Processor</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="api_key">API Key</label>
          <input
            type="text"
            id="api_key"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Enter your API Key"
            required
          />
        </div>
        <div>
          <label htmlFor="wallet_address">Wallet Address</label>
          <input
            type="text"
            id="wallet_address"
            value={walletAddress}
            onChange={(e) => setWalletAddress(e.target.value)}
            placeholder="Enter your Wallet Address"
            required
          />
        </div>
        <button type="submit">Process Wallet</button>
      </form>

      {responseMessage && (
        <div
          className={`response-message ${error ? "error" : ""}`}
        >
          {responseMessage}
          {csvPath && !error && (
            <p>
              <a
                href={`/download_csv?path=${encodeURIComponent(csvPath)}`}
                target="_blank"
                rel="noopener noreferrer"
                style={{ textDecoration: "underline", color: "var(--primary-color)" }}
              >
                Download CSV
              </a>
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default WalletProcessor;
