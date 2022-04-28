let timers = {};

const generateText = (htmlForm, textForm) => {
	console.log('oju');
};

document.querySelectorAll('form.email').forEach((form) => {

	timers[form.id] = null;

	form.elements['html_body'].addEventListener("keyup", e => {
		if(timers[form.id]) {
			clearTimeout(timers[form.id]);
		}
		timers[form.id] = setTimeout(() => {
			if(form.elements['autogenerate_text'].checked) {
				generateText(form.elements['html_body'], form.elements['text_body']);
			}
			timers[form.id] = null;
		}, 500);		
	});
});