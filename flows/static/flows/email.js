/* Strips html leaving only text */
const stripHtml = (html) => (new DOMParser().parseFromString(html, 'text/html')).body.textContent || "";

for (const form of document.querySelectorAll('form.email')) {

	let timer = null;
	const iframePreview = form.querySelector('iframe'),
		textPreview = form.querySelector('pre.text'),
		htmlBodyControl = form.elements['html_body'],
		textBodyControl = form.elements['text_body'],
		autoGenerateTextControl = form.elements['autogenerate_text'],
		previewContextControl = form.elements['preview_context'],
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
					textBodyControl.value = stripHtml(htmlBodyControl.value);
				}
				/* Keep previews updated */
				let formData = new FormData();
				formData.set('mode', 'email');
				formData.set('context', previewContextControl.value);
				formData.set('message', htmlBodyControl.value);
				fetch(previewUrl, { method: 'POST', body: formData }).then(async response => iframePreview.srcdoc = await response.text());
				formData.set('mode', 'plain');
				formData.set('message', textBodyControl.value);
				fetch(previewUrl, { method: 'POST', body: formData }).then(async response => textPreview.textContent = await response.text());
				timer = null;
			}, 500);
		};
	update();
	form.addEventListener("keyup", update);
	form.addEventListener('reset', update);
	/* Update text on enable control */
	autoGenerateTextControl.addEventListener("change", update);

	
}