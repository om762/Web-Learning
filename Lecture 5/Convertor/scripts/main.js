document.addEventListener('DOMContentLoaded', async () => {
    const fromCurrencySelect = document.getElementById('from-currency');
    const toCurrencySelect = document.getElementById('to-currency');
    const amountInput = document.getElementById('amount');
    const resultSection = document.getElementById('result');
    
    // Fetch and populate currency dropdowns
    try {
        const response = await fetch('https://api.exchangerate-api.com/v4/latest/USD'); // Use your preferred base currency
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();

        const currencies = Object.keys(data.rates);
        populateCurrencyDropdowns(currencies);
    } catch (error) {
        console.error('Error fetching currency list:', error);
        resultSection.textContent = 'Error fetching currency list. Please try again later.';
    }

    function populateCurrencyDropdowns(currencies) {
        currencies.forEach(currency => {
            const optionFrom = document.createElement('option');
            optionFrom.value = currency;
            optionFrom.textContent = currency;
            fromCurrencySelect.appendChild(optionFrom);

            const optionTo = document.createElement('option');
            optionTo.value = currency;
            optionTo.textContent = currency;
            toCurrencySelect.appendChild(optionTo);
        });
    }

    async function convertCurrency() {
        const amount = amountInput.value;
        const fromCurrency = fromCurrencySelect.value;
        const toCurrency = toCurrencySelect.value;

        if (!amount || isNaN(amount)) {
            resultSection.textContent = '';
            return;
        }

        try {
            const response = await fetch(`https://api.exchangerate-api.com/v4/latest/${fromCurrency}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();

            const rate = data.rates[toCurrency];
            const convertedAmount = (amount * rate).toFixed(2);

            resultSection.textContent = `${amount} ${fromCurrency} = ${convertedAmount} ${toCurrency}`;
        } catch (error) {
            console.error('Error fetching exchange rates:', error);
            resultSection.textContent = 'Error fetching exchange rates. Please try again later.';
        }
    }

    // Add event listeners for real-time conversion
    amountInput.addEventListener('input', convertCurrency);
    fromCurrencySelect.addEventListener('change', convertCurrency);
    toCurrencySelect.addEventListener('change', convertCurrency);
});
