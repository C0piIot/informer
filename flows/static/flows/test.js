const form = document.getElementById('form-test-flow'),
	curlExcample = document.getElementById('id_curl_example'),
	apiUrl = curlExcample.dataset.urlEndpoint,
	privateKey = curlExcample.dataset.privateKey,
	event = curlExcample.dataset.event,
	update = async () => {
		const body = new URLSearchParams({
			"event" : event,
			"contact_key" : form.elements['contact_key'].value,
			"event_payload" : form.elements['event_payload'].value,
		});
		curlExcample.value = `curl '${apiUrl}' -H 'Authorization: Bearer ${privateKey}' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Accept:application/json; version=1' --data-raw '${body}'`;
	};
update();
form.addEventListener("keyup", update);
form.addEventListener('reset', update);