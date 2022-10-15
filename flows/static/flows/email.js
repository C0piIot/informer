/* Strips html leaving only text */
const stripHtml = (html) => (new DOMParser().parseFromString(html, 'text/html')).body.textContent || "";

for (const form of document.querySelectorAll('form.email')) {

	let timer = null;
	const iframePreview = form.querySelector('iframe'),
		textPreview = form.querySelector('pre'),
		htmlBodyControl = form.elements['html_body'],
		textBodyControl = form.elements['text_body'],
		autoGenerateTextControl = form.elements['autogenerate_text'],
		previewContextControl = form.elements['preview_context'],
		previewUrl = form.querySelector("[data-render-mail-url]").dataset.renderMailUrl,
	    update = async () => {
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
				const response = await (await fetch(previewUrl, { method: 'POST', body: new FormData(form) })).json();
				iframePreview.srcdoc = response['html_preview'];
				textPreview.textContent = response['text_preview'];
				timer = null;
			}, 500);
		};

	[htmlBodyControl, textBodyControl, previewContextControl].forEach((e) => e.addEventListener("keyup", update));

	/* Update text on enable control */
	autoGenerateTextControl.addEventListener("change", () => {
		if(autoGenerateTextControl.checked) {
			update();
		}
	});

	form.addEventListener('reset', () => htmlBodyControl.dispatchEvent(new Event('keyup')));

}