const withSentry = require('serverless-sentry-lib');
const AWS = require('aws-sdk');
const csv = require('csvtojson');
const UUID = require('uuid');

AWS.config.update({region: 'us-east-1'});

const HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Credentials': true,
  'Access-Control-Allow-Headers': '*',
};


module.exports.get_schedule = withSentry(async (event) => {
  const ddb = new AWS.DynamoDB.DocumentClient();
  const params = {
    TableName: process.env.EXPO_TABLE,
  };

  const result = await ddb.scan(params).promise();

  // Returns status code 200 and JSON string of 'result'
  return {
    statusCode: 200,
    body: JSON.stringify(result.Items),
    headers: HEADERS,
  };
});

module.exports.post_schedule = withSentry(async (event) => {
  const ddb = new AWS.DynamoDB.DocumentClient();
  const body = JSON.parse(event.body);

    // checks if any field is missing to create a  user
  if (!body.email
    || !body.full_name
    || !body.access_level // TODO refactor to `role` instead of `access_level`?
    || !body.group
    || !body.campfire_team) { // Campfire team is a Bitcamp-specific field ('red' | 'green' | 'blue')
    return {
      statusCode: 400,
      body: ' is missing a field',
    };
  }

  body.id = emailToUserId(body.email);

  const params = {
    TableName: process.env.USERS_TABLE,
    Item: {},
  };

  // dynamically add post request body params to document
  Object.keys(body).forEach((k) => {
    params.Item[k] = body[k];
  });
  

  body.setRegistrationStatus = true;

  // Send the user an invite email (for Bitcamp, we send the invite emails separately from adding users)
  // await sendLoginLinkEmail(body.id, true, false);

  // Returns status code 200 and JSON string of 'result'
  return {
    statusCode: 200,
    body: JSON.stringify(params.Item),
    headers: HEADERS,
  };
});
