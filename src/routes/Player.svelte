<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import { isAudioElement } from '$lib/utils/typeGuard';

	export let isRecording: boolean;
	export let chunks: Blob[];
	let isRecorderReady = false;
	let mediaRecorder: MediaRecorder | null = null;

	setupMediaRecorder().then((recorder) => {
		mediaRecorder = recorder || null;
		isRecorderReady = true;
	});

	async function setupMediaRecorder() {
		if (typeof window === 'undefined') return;
		const player = document.querySelector('#player');

		if (!player) {
			console.error('Failed to find player element.');
			return;
		}

		const stream = await navigator.mediaDevices.getUserMedia({
			video: false,
			audio: true
		});

		if (!MediaRecorder.isTypeSupported('audio/webm')) {
			console.warn('audio/webm is not supported');
		}

		const mediaRecorder = new MediaRecorder(stream, {
			mimeType: 'audio/webm'
		});

		mediaRecorder.addEventListener('dataavailable', (event) => {
			chunks.push(event.data);
		});

		mediaRecorder.addEventListener('stop', () => {
			const blob = new Blob(chunks, { type: 'audio/webm' });
			if (player && isAudioElement(player)) {
				URL.revokeObjectURL(player.src);
				player.src = URL.createObjectURL(blob);
			} else {
				console.error('Failed to find player element.');
			}
		});

		return mediaRecorder;
	}

	function onClickStart(recorder: MediaRecorder | null) {
		if (!recorder) return;
		recorder.start();
		chunks = [];
		isRecording = true;
	}

	const onClickStop = (recorder: MediaRecorder | null) => {
		if (!recorder) return;
		recorder.stop();
		isRecording = false;
	};
</script>

{#if isRecorderReady}
	{#if !mediaRecorder}
		<p>MediaRecorder is not ready.</p>
	{/if}
{:else}
	<p>MediaRecorder is being prepared...</p>
{/if}

<div>
	<Button
		onClick={() => onClickStart(mediaRecorder)}
		disabled={!isRecorderReady || isRecording}
		id="buttonStart"
		className={`${isRecording ? 'is-light' : 'is-primary'}`}
	>
		Start
	</Button>
	<Button
		onClick={() => onClickStop(mediaRecorder)}
		disabled={!isRecorderReady || !isRecording}
		id="buttonStop"
		className={`${isRecording ? 'is-danger' : 'is-light'}`}
	>
		Stop
	</Button>
</div>

<audio controls id="player" aria-disabled={!isRecorderReady} />
