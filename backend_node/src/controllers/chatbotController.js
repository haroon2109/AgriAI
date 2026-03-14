exports.getResponse = async (req, res) => {
  const { message } = req.body;
  const lowerMsg = message.toLowerCase();

  let response = "I'm sorry, I don't have information on that yet. You can ask about shipping, returns, or crop advice!";

  if (lowerMsg.includes('shipping')) {
    response = "We offer standard shipping (3-5 days) and express shipping (1-2 days) across Tamil Nadu.";
  } else if (lowerMsg.includes('return')) {
    response = "Items can be returned within 15 days of delivery if they are in original condition.";
  } else if (lowerMsg.includes('payment')) {
    response = "We accept UPI, Credit/Debit cards, and Cash on Delivery for seeds and tools.";
  } else if (lowerMsg.includes('paddy') || lowerMsg.includes('rice')) {
    response = "For Paddy, ensure proper water levels during the vegetative phase and monitor for stem borers.";
  }

  res.json({ response });
};
