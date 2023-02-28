<script lang="ts">
	import Icon from '@iconify/svelte';
	import { fade } from 'svelte/transition';
	let userName: string;
	let password: string;
	let confirmPassword: string;
	let respcode: number;
	let correctRegister = false;
	let url = 'http://192.168.1.138:8081/api/register';
	function constrain(input: string, min: number, max: number) {
		return input.length >= min && input.length <= max;
	}

	$: correctRegister =
		constrain(userName || '', 6, 20) &&
		constrain(password || '', 6, 30) &&
		password === confirmPassword;

	function handleSubmit() {
		const data = { username: userName, password: password };

		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		})
			.then((response) => response.status)
			.then((data) => {
				respcode = data;
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	}

	$: console.log(respcode);
</script>

<div
	class="flex flex-col justify-center bg-original-card-bg-dark px-20 rounded-lg min-w-full align-middle"
>
    {#if respcode == 201}
    <div class="h-1/4 flex flex-col justify-center">
        <div class="text-9xl mx-auto text-original-success">
            <Icon icon="ooui:success" />
        </div>
        <span class="text-2xl text-original-success mt-4">Success</span>
    </div>
    {/if}

    {#if respcode == 409}
    <div class="h-1/4 flex flex-col justify-center">
        <div class="text-9xl mx-auto text-red-500">
            <Icon icon="emojione-monotone:heavy-multiplication-x" />
        </div>
        <span class="text-2xl text-red-500 mt-4">This username has already been registered!</span>

    </div>
    {/if}

	<div class="flex flex-col justify-center mt-10">
		<div class="text-center mb-10 text-xl">
			<span class:warning={!constrain(userName || '', 6, 20)} class="text-slate-400">
				Usernames must be between 6 and 20 characters long.
			</span>
			<br />
			<span
				class:warning={!constrain(confirmPassword || '', 6, 30) || confirmPassword !== password}
				class="text-slate-400"
			>
				Passwords must be between 6 and 30 characters long and match.
			</span>
		</div>

		<form class="mb-10">
			<input
				type="text"
				class:good={constrain(userName || '', 6, 20)}
				class="w-2/3 h-10 mx-auto my-2 text-original-base  bg-slate-700 outline-none rounded-lg border-original-muted hover:bg-original-input-hover text-center transition-colors"
				placeholder="Username..."
				bind:value={userName}
			/>

			<input
				type="password"
				class:good={constrain(password || '', 6, 30)}
				class="w-2/3 h-10 mx-auto my-2 text-original-base  bg-slate-700 outline-none rounded-lg border-original-muted hover:bg-original-input-hover text-center transition-colors"
				placeholder="Password"
				bind:value={password}
			/>

			<input
				type="password"
				class:good={constrain(confirmPassword || '', 6, 30) && confirmPassword === password}
				class="w-2/3 h-10 mx-auto my-2 text-original-base  bg-slate-700 outline-none rounded-lg border-original-muted hover:bg-original-input-hover text-center transition-colors"
				placeholder="Confirm password"
				bind:value={confirmPassword}
			/>
		</form>
		<button
			type="submit"
			class="w-1/3 mx-auto rounded-xl py-2 text-stone-200"
			disabled={!correctRegister}
			on:click={() => handleSubmit()}>Submit</button
		>
	</div>
</div>

<style>
	.good {
		background-color: rgba(10, 83, 0);
	}

	.good:hover {
		background-color: rgba(49, 153, 1, 0.479);
		opacity: 70%;
	}

	.warning {
		color: rgba(216, 33, 33, 0.87);
	}

	:disabled {
		background-color: rgb(58, 58, 58);
		color: rgb(148, 148, 148);
	}
	button:not(:disabled) {
		background-color: rgb(10, 83, 0);
		color: rgb(148, 148, 148);
	}
</style>
