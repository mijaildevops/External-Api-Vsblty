<?php
// allow CORS access
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");

?>

<?php

//url to get the access token
$url = "https://vsblty-apiv2-qa.azurewebsites.net/token";

// Import 
// Enter your access keys
// --------------------------------------------------------------
// Access parameters (Api Key and user credentials)
// --------------------------------------------------------------
$client_credentials = "client_credentials";
$client_id = "F4DAB8A1-774D-4957-8497-FD4D73361E32";
$client_secret = "g44bIeDH/YRjeM7IpkOwyfjr8kRUOVUxE/h3swR6RCCs2SPP3eDq4VVXo124YIH3084+nJvAG4SmMVcOxx7JYA==";

// Access parameters are assigned as an array that will be sent Curl
$fields = array(
	'grant_type' => $client_credentials,
	'client_id' => $client_id,
	'client_secret' => $client_secret

);

$curl = \curl_init();

\curl_setopt_array($curl, array(
	CURLOPT_URL => $url,
	CURLOPT_RETURNTRANSFER => true,
	CURLOPT_ENCODING => "",
	CURLOPT_MAXREDIRS => 10,
	CURLOPT_TIMEOUT => 600,
	CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
	CURLOPT_HTTPHEADER => $fields,
	CURLINFO_HEADER_OUT => true,
	CURLOPT_POST => true,
	CURLOPT_POSTFIELDS => http_build_query($fields),

));

// we execute the Curl request
$response = curl_exec($curl);

// we get the Token from the request
$response = [
  'Token' => substr($response, 17, 278),
];

?>


<?php

// This is the token
$Token = $response['Token'];

// Important 
// --------------------------------------------------------------
// Endpoint you want to consult
// --------------------------------------------------------------
//$EndpointData = "ebbc2f54-5149-4e73-ab12-d5dccfe63769";   // laptop
$EndpointData = "4a516236-f23c-4b10-802f-9a9b68c50dd0";   // Main Home
$EndpointData = "39127806-4531-4de9-9881-4284f8d6017a";   // Santiago


// Url with the Id of the endpoint that you want to obtain the data
$requestUrl = 'https://vsblty-apiv2-qa.azurewebsites.net/api/LiveEndpointData/'. $EndpointData .'/true';

// The token is sent Along with the url
$headers = array("Authorization: Bearer $Token");
 
// we make the request to obtain the data sent by the endpoint
$ch = curl_init($requestUrl);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_POSTFIELDS, $requestUrl);
$result = curl_exec($ch);

$result=  json_decode($result);

?>

