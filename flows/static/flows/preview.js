const previewUrl = document.querySelector("[data-preview-url]").dataset.previewUrl;
for (const form of document.getElementsByTagName('form')) {
	const targets = form.querySelectorAll('[data-preview-from]');
	if(!targets.length) {
		continue;
	}
	let timer = null;
	const update = async () => {
		/* Use a timer to update preview and text only once in a while */
		if(timer) {
			clearTimeout(timer);
		}
		timer = setTimeout(async () => {
			for (const target of targets) {
				const source = form.elements[target.dataset.previewFrom];
				if(source.value) {
					const formData = new FormData();
					formData.set('mode', target.dataset.previewMode ?? 'html');
					formData.set('context', form.elements[target.dataset.previewContext ?? 'preview_context'].value ?? '');
					formData.set('message', source.value);
					fetch(previewUrl, { method: 'POST', body: formData }).then(async response => target.textContent = await response.text());
				} else {
					target.textContent = '';
				}

			}
			timer = null;
		}, 500);
	};
	update();
	form.addEventListener("keyup", update);
	form.addEventListener('reset', update);
}
