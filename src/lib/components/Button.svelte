<script lang="ts">
	export let onClick: () => void;
	export let disabled = false;
	export let id = '';
	export let className = '';
</script>

<button {id} type="button" class={`button ${className}`} on:click={onClick} {disabled}>
  {#if $$slots.icon}
    <span class="mr-1 mt-1">
      <slot name="icon" />
    </span>
  {/if}
	<slot />
</button>
