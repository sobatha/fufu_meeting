<script lang='ts'>
	let isRecording = false;
	let chunks: Blob[] = [];
	let mediaRecorder = main();

	async function main() {
		if (typeof window === 'undefined') return;
		const player = document.querySelector('#player');
		URL.revokeObjectURL(player.src)

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
			// player.src = URL.createObjectURL(event.data);
			chunks.push(event.data);
		});

		mediaRecorder.addEventListener('stop', () => {
			const blob = new Blob(chunks, { type: 'audio/webm' });
			URL.revokeObjectURL(player.src)
			player.src = URL.createObjectURL(blob);
			// Clear the chunks for next recording
			chunks = [];
			// URL.revokeObjectURL()
		});
		
		return mediaRecorder
	}

	function onClickStart (recorder: any) {
		// if(!recorder) return;
		recorder.start();
		isRecording = true;
		// return null
	};

	const onClickStop = (recorder) => {
		if(!recorder) return
		recorder.stop();
		isRecording = false;
		// return null
	};


</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>
{#await mediaRecorder then recorder}
<div>
	{ recorder }
	<button type="button" id="buttonStart" on:click={()=>onClickStart(recorder)} disabled={isRecording}>Start</button>
	<button type="button" id="buttonStop" on:click={()=>onClickStop(recorder)} disabled={!isRecording}>Stop</button>
</div>
{/await}
<div>
	<audio controls id="player" />
</div>

<style>
</style>
