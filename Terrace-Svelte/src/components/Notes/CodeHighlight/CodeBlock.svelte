<script>
	import ada from 'svelte-highlight/languages/ada';
	import actionscript from 'svelte-highlight/languages/actionscript';
	import arduino from 'svelte-highlight/languages/arduino';
	import autohotkey from 'svelte-highlight/languages/autohotkey';
	import bash from 'svelte-highlight/languages/bash';
	import brainfuck from 'svelte-highlight/languages/brainfuck';
	import c from 'svelte-highlight/languages/c';
	import lisp from 'svelte-highlight/languages/lisp';
	import clojure from 'svelte-highlight/languages/clojure';
	import cmake from 'svelte-highlight/languages/cmake';
	import cpp from 'svelte-highlight/languages/cpp';
	import css from 'svelte-highlight/languages/css';
	import d from 'svelte-highlight/languages/d';
	import dart from 'svelte-highlight/languages/dart';
	import javascript from 'svelte-highlight/languages/javascript';
	import python from 'svelte-highlight/languages/python';
	import pyrepl from 'svelte-highlight/languages/python-repl';
	import ruby from 'svelte-highlight/languages/ruby';
	import rust from 'svelte-highlight/languages/rust';
	import plaintext from 'svelte-highlight/languages/plaintext';

	import { Highlight, HighlightSvelte } from "svelte-highlight";
	import Children from 'svelte-exmarkdown/renderer/Children.svelte';
	import oneDark from 'svelte-highlight/styles/atom-one-dark';
	const languages = {
		'language-ada': ada,
		'language-as': actionscript,
		'language-as3': actionscript,
		'language-arduino': arduino,
		'language-ahk': autohotkey,
		'language-bash': bash,
		'language-brainfuck': brainfuck,
		'language-bf': brainfuck,
		'language-c': c,
		'language-cl': lisp,
		'language-clojure': clojure,
		'language-clj': clojure,
		'language-cmake': cmake,
		'langauge-cpp': cpp,
		'language-css': css,
		'language-d': d,
		'language-js': javascript,
		'language-py': python,
		'language-rb': ruby,
		'language-rs': rust,
	};

	export let children;
	export let theme = oneDark;
	let code;
	let _class;
	let language;
	$: {
		code = children[0].children[0].value;
		_class = children[0].properties.class;

		language = '';
		if(_class && languages.hasOwnProperty(_class)) {
			language = languages[_class];
		} else {
			language = plaintext;
		}

		console.log(code);
		console.log(language);
	}
</script>


<svelte:head>
	{@html theme}
</svelte:head>

{#if _class === 'language-svelte'}
	<HighlightSvelte {code} />
{:else}
	<Highlight {language} {code} />
{/if}

