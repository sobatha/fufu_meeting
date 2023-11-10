<script lang="ts">
	import Player from './Player.svelte';

	let isRecording = false;
	let chunks: Blob[] = [];



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


		<Player
			{isRecording}
			{chunks}
		/>

		<!-- <Button onClick={uploadRecording} className="is-primary">
			<svelte:fragment slot="icon">
				<SendIcon />
			</svelte:fragment>
			送信
		</Button> -->
	<!-- {:else} -->
		<p>MediaRecorder is not ready.</p>


<style>
</style>
