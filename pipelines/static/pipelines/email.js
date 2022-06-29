/* Strips html leaving only text */
const stripHtml = (html) => (new DOMParser().parseFromString(html, 'text/html')).body.textContent || "";

for (const form of document.querySelectorAll('form.email')) {

	let timer = null;
	const iframePreview = form.querySelector('iframe'), 
		htmlBodyControl = form.elements['html_body'],
		textBodyControl = form.elements['text_body'],
		autoGenerateTextControl = form.elements['autogenerate_text'];

	htmlBodyControl.addEventListener("keyup", async () => {
		
		/* Use a timer to update preview and text only once in a while */
		if(timer) {
			clearTimeout(timer);
		}
		timer = setTimeout(async () => {
			/* Keep text updated if enabled */
			if(autoGenerateTextControl.checked) {
				textBodyControl.value = stripHtml(htmlBodyControl.value);
			}

			/* Keep preview updated */
			const response = await fetch(iframePreview.dataset.renderMailUrl, { method: 'POST', body: htmlBodyControl.value });
			iframePreview.srcdoc = await response.text();
			timer = null;
		}, 500);
	});

	/* Update text on enable control */
	autoGenerateTextControl.addEventListener("change", () => {
		if(autoGenerateTextControl.checked) {
			textBodyControl.value = stripHtml(htmlBodyControl.value);
		}
	});
}