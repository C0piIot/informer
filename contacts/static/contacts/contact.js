//Toggle channel data forms 
document.querySelectorAll('form.contact').forEach(form => {
	const toggleChannel = (idChannel, enabled) => {
		form.querySelector(`button.channel-${idChannel}`).hidden = !enabled;
		form.querySelectorAll(`div.channel-${idChannel} :is(input,select,textarea,button)`).forEach(formControl => formControl.disabled = !enabled);
	};

	form.querySelectorAll('input[name="channels"]').forEach(checkbox => {
		checkbox.addEventListener('change', () => toggleChannel(checkbox.value, checkbox.checked));
		toggleChannel(checkbox.value, checkbox.checked);
	});
});