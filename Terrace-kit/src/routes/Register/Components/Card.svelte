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
	class="flex flex-col justify-center bg-original-card-bg-dark px-20 rounded-lg w-1/2 mx-auto align-middle py-4"
>
    <div class="h-1/4 flex flex-col justify-center">
    {#if respcode == 201}

        <div class="text-6xl mx-auto text-original-success">
            <Icon icon="ooui:success" />
        </div>
        <span class="text-2xl text-original-success mt-4">Success</span>
    {/if}
    {#if respcode == 409}
    <div class="h-1/4 flex flex-col justify-center">
        <div class="text-6xl mx-auto text-red-500">
            <Icon icon="emojione-monotone:heavy-multiplication-x" />
        </div>
        <span class="text-2xl text-red-500 mt-4">This username has already been registered!</span>

    </div>
    {/if}
    </div>

    

	<div class="flex flex-col justify-center mt-10">
		<div class="text-center mb-10 text-md">
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
            <span class="block w-full text-left text-original-base text-sm">Username</span>
			<input
				type="text"
				
				class="w-full h-10 mx-auto text-original-base  bg-slate-700 outline-none rounded-lg border-original-muted hover:bg-original-input-hover text-center transition-colors"
				placeholder="Username..."
				bind:value={userName}
			/>
            <span class="block w-full text-left text-original-base mt-4 text-sm">Password</span>
			<input
				type="password"
				
				class="w-full h-10 mx-auto text-original-base  bg-slate-700 outline-none rounded-lg border-original-muted hover:bg-original-input-hover text-center transition-colors"
				placeholder="Password"
				bind:value={password}
			/>
            <span class="block w-full text-left text-original-base mt-4 text-sm">Confirm Password</span>
			<input
				type="password"
				
				class="w-full h-10 mx-auto text-original-base  bg-slate-700 outline-none rounded-lg border-original-muted hover:bg-original-input-hover text-center transition-colors"
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
