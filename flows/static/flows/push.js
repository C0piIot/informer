for (const form of document.querySelectorAll('form.push')) {

	let timer = null;
	const titlePreview = form.querySelector('pre.title'),
		urlPreview = form.querySelector('pre.url'),
		bodyPreview = form.querySelector('pre.body'),
		titleControl = form.elements['title'],
		urlControl = form.elements['url'],
		bodyControl = form.elements['body'],
		previewContextControl = form.elements['preview_context'],
		previewUrl = document.querySelector("[data-preview-url]").dataset.previewUrl,
	    update = async () => {
			/* Use a timer to update preview and text only once in a while */
			if(timer) {
				clearTimeout(timer);
			}
			timer = setTimeout(async () => {
				/* Keep previews updated */
				let formData = new FormData();
				formData.set('mode', 'plain');
				formData.set('context', previewContextControl.value);
				formData.set('message', titleControl.value);
				fetch(previewUrl, { method: 'POST', body: formData }).then(async response => titlePreview.textContent = await response.text());
				formData.set('mode', 'plain');
				formData.set('message', urlControl.value);
				fetch(previewUrl, { method: 'POST', body: formData }).then(async response => urlPreview.textContent = await response.text());
				formData.set('message', bodyControl.value);
				fetch(previewUrl, { method: 'POST', body: formData }).then(async response => bodyPreview.textContent = await response.text());
				timer = null;
			}, 500);
		};
	update();
	form.addEventListener("keyup", update);
	form.addEventListener('reset', update);
}