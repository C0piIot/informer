const form = document.getElementById('form-test-flow'),
	input = document.getElementById('id_curl_example'),
	update = () => 
		input.value = 
			`curl '${input.dataset.urlEndpoint}' -H 'Authorization: Bearer ${input.dataset.privateKey}' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept:application/json; version=1' --data-raw '${new URLSearchParams({
				"event" : input.dataset.event,
				"contact_key" : form.elements['contact_key'].value,
				"event_payload" : form.elements['event_payload'].value,
			})}'`;

update();
form.addEventListener("keyup", update);
form.addEventListener('reset', update);

document.getElementById('curl-example-copy')
	.addEventListener('click', () => navigator.clipboard.writeText(input.value));