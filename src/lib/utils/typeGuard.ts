export const isAudioElement = (element: Element): element is HTMLAudioElement => {
	return element.tagName === 'AUDIO';
};
