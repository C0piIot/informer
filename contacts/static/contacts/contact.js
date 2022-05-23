//Toggle channel data forms 

for (const form of document.querySelectorAll('form.contact')) {
	const toggleChannel = (idChannel, enabled) => {
		form.querySelector(`button.channel-${idChannel}`).hidden = !enabled;
		form.querySelectorAll(`div.channel-${idChannel} :is(input,select,textarea,button)`).forEach(formControl => formControl.disabled = !enabled);
	};

	for (const checkbox of form.querySelectorAll('input[name="channels"]')) {
		checkbox.addEventListener('change', () => toggleChannel(checkbox.value, checkbox.checked));
		toggleChannel(checkbox.value, checkbox.checked);
	}
	
	let timer = null; // Usamos un timer para resetear cuando hemos forzado una pestaña
	form.addEventListener('invalid', e => {
		const tab = e.srcElement.closest('.tab-pane');
		if(timer) { //Ya habiamos forzado pestaña, si no es la actual no intentemos mostrar el error
			if(!tab.classList.contains('active')) {
				e.preventDefault();
			}
		} else {
			timer = setTimeout(() => timer = null);
			const trigger = document.getElementById(tab.getAttribute('aria-labelledby'));
			(new bootstrap.Tab(trigger)).show();
		}
	}, true);
	
}