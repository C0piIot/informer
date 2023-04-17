/* Strips html leaving only text */
const stripHtml = (html) => (new DOMParser().parseFromString(html, 'text/html')).body.textContent || "";
const removeEmptyLines = (text) => text.replace(/^(\s+\n)+/gm, '\n')
const removeExtraSpaces = (text) => text.replace(/(\s+)(^\s)/g, ' ')

for (const form of document.querySelectorAll('form.email')) {

	let timer = null;
	const iframePreview = form.querySelector('iframe'),
		htmlBodyControl = form.elements['html_body'],
		textBodyControl = form.elements['text_body'],
		autoGenerateTextControl = form.elements['autogenerate_text'],
		previewUrl = document.querySelector("[data-preview-url]").dataset.previewUrl,
	    update = async () => {
			/* Use a timer to update preview and text only once in a while */
			if(timer) {
				clearTimeout(timer);
			}
			textBodyControl.readOnly = autoGenerateTextControl.checked;
			timer = setTimeout(async () => {
				/* Keep text updated if enabled */
				if(autoGenerateTextControl.checked) {
					textBodyControl.value = 
						removeExtraSpaces(
							removeEmptyLines(
								stripHtml(
									htmlBodyControl.value
								)
							)
						);
					textBodyControl.dispatchEvent(new Event('change'));
				}
				/* Keep preview updated */
				let formData = new FormData();
				formData.set('mode', 'email');
				formData.set('message', htmlBodyControl.value);
				fetch(previewUrl, { method: 'POST', body: formData }).then(async response => iframePreview.srcdoc = await response.text());
				timer = null;
			}, 500);
		};
	update();
	form.addEventListener("keyup", update);
	form.addEventListener('reset', update);
	/* Update text on enable control */
	autoGenerateTextControl.addEventListener("change", update);

	
}