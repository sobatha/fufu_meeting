<script lang="ts">
	import Button from '$lib/components/Button.svelte';
	import SendIcon from '$lib/components/icons/SendIcon.svelte';

	let isRecording = false;
	let chunks: Blob[] = [];
	let mediaRecorder = setupMediaRecorder();

	async function setupMediaRecorder() {
		if (typeof window === 'undefined') return;
		const player = document.querySelector('#player');

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
			URL.revokeObjectURL(player.src);
			player.src = URL.createObjectURL(blob);
		});

		return mediaRecorder;
	}

	function onClickStart(recorder: any) {
		recorder.start();
		chunks = [];
		isRecording = true;
	}

	const onClickStop = (recorder: any) => {
		recorder.stop();
		isRecording = false;
	};

	async function uploadRecording() {
		if (chunks.length === 0) return;

		const blob = new Blob(chunks, { type: 'audio/webm' });
		const formData = new FormData();
		formData.append('audio', blob, 'audio.webm');

		try {
			const response = await fetch('/upload', {
				method: 'POST',
				body: formData
			});

			if (response.ok) {
				console.log('Successfully uploaded recording.');
			} else {
				console.log('Failed to upload recording.');
			}
		} catch (err) {
			console.error('Error uploading recording:', err);
		}
	}
</script>

{#await mediaRecorder then recorder}
	<div>
		<Button
			onClick={() => onClickStart(recorder)}
			disabled={isRecording}
			id="buttonStart"
			className={`${isRecording ? 'is-light' : 'is-primary'}`}
		>
			Start
		</Button>
		<Button
			onClick={() => onClickStop(recorder)}
			disabled={!isRecording}
			id="buttonStop"
			className={`${isRecording ? 'is-danger' : 'is-light'}`}
		>
			Stop
		</Button>
	</div>
	<Button onClick={uploadRecording} className="is-primary">
		<svelte:fragment slot="icon">
			<SendIcon />
		</svelte:fragment>
		送信
	</Button>
{/await}

<div>
	<audio controls id="player" />
</div>

<style>
</style>
