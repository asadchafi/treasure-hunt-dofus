const puppeteer = require('puppeteer-extra');
const axios = require('axios'); // Use axios to make HTTP requests

// Add the stealth plugin to evade detection techniques
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

// Launch the browser with the option to show the UI
puppeteer.launch({ headless: false }).then(async browser => {
  console.log('Running tests..');
  const page = await browser.newPage();

  // Enable request interception to capture outgoing requests
  await page.setRequestInterception(true);

  // Variable to store the token data
  let token = null;

  // Listen for intercepted requests to capture the token
  page.on('request', interceptedRequest => {
    let url = interceptedRequest.url();
    
    // Check if the URL matches the API you're interested in
    if (url.startsWith("https://api.dofusdb.fr/treasure-hunt")) {
      
      // Capture and parse the request headers
      let headers = interceptedRequest.headers();

      // Check if the token exists in the headers and extract it
      if (headers['token']) {
        token = headers['token'];  // Store the token in the variable
        console.log('Token found:', token);  // Log the token
      }
    }

    // Continue the request after interception
    interceptedRequest.continue();
  });

  // Go to the page where the API call is triggered
  await page.goto('https://dofusdb.fr/en/tools/treasure-hunt');

  // Polling loop to check for the token every 2 seconds
  const waitForToken = async () => {
    return new Promise((resolve, reject) => {
      const interval = setInterval(() => {
        if (token) {
          clearInterval(interval); // Stop polling once token is found
          resolve(token); // Resolve the promise with the token
        }
      }, 1000); // Check every 1 seconds

      // Timeout after 30 seconds if token is not found
      setTimeout(() => {
        clearInterval(interval);
        reject(new Error('Token not found after waiting for 30 seconds'));
      }, 30000);
    });
  };

  // Wait for the token to be generated
  try {
    const generatedToken = await waitForToken();
    console.log('Generated Token:', generatedToken);

    // Send GET request using the token as a Bearer token
    const url = 'https://dofus-map.com/huntTool/getData.php?x=-6&y=-7&direction=right&world=0&language=en';
    try {
      const response = await axios.get(url, {
        headers: {
          'Authorization': `Bearer ${generatedToken}`,
        }
      });
      // Log the response JSON object
      console.log('Response from API:', response.data);
    } catch (error) {
      console.error('Error sending GET request:', error);
    }
  } catch (error) {
    console.error(error.message); // Handle the error if token is not found
  }
});
