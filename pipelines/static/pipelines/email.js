/* Strips html leaving only text */
const stripHtml = (html) => (new DOMParser().parseFromString(html, 'text/html')).body.textContent || "";

for (const form of document.querySelectorAll('form.email')) {

	let timer = null;
	const iframePreview = form.querySelector('iframe'), 
		htmlBodyControl = form.elements['html_body'],
		textBodyControl = form.elements['text_body'],
		autoGenerateTextControl = form.elements['autogenerate_text'];

	htmlBodyControl.addEventListener("keyup", () => {
		
		/* Use a timer to update preview and text only once in a while */
		if(timer) {
			clearTimeout(timer);
		}
		timer = setTimeout(() => {
			/* Keep preview updated */
			iframePreview.srcdoc = htmlBodyControl.value;

			/* Keep text updated if enabled */
			if(autoGenerateTextControl.checked) {
				textBodyControl.value = stripHtml(htmlBodyControl.value);
			}
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