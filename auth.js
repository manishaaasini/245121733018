const axios = require('axios');

const authorizeCompany = async () => {
  const authUrl = 'http://20.244.56.144/test/auth';
  const authData = {
    companyName: 'goMart',
    clientID: '5c5c398d-253c-4854-b6d2-3d25e3fd5234',
    clientSecret: 'KyQUHafaevMpeEzL',
    ownerName: 'Manisha Asini',
    ownerEmail: '245121733018@mvsrec.edu.in',
    rollNo: '2451-21-733-018'
  };

  try {
    // Request the authorization token
    const authResponse = await axios.post(authUrl, authData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log('Authorization Token Response:', authResponse.data);

  } catch (error) {
    console.error('Error:', error.response ? error.response.data : error.message);
  }
};

authorizeCompany();