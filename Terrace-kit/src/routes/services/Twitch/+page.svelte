<script>
    import ToggleButton from "../Button/ToggleButton.svelte";
</script>

<div class="flex flex-row justify-center mt-10 items-center">
    <div class="h-1/3 mt-5 flex justify-center align-top">
        <ToggleButton 
            OniconName="mdi:microphone-plus" commandType="TTS" buttonOnCommand={true}
            OfficonName="mdi:microphone-minus" buttonOffCommand={false} name="TTS" 
        />
    </div>
</div>

