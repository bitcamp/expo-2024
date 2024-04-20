<template>
    <div class="entire-container">

        <div v-for="(teamDetail, index) in sortedTeamDetails" :key="index">
            <div class="top-row" v-if="filtered.includes(teamDetail[1]) && (challengeDetails === '' || teamDetail[2].some(challenge => challengeDetails.includes(challenge[0]))) &&
            (projectType === 'all' ||
                (projectType === 'virtual' && teamDetail[0][0] === 'No') ||
                (projectType === 'in-person' && teamDetail[0][0] !== 'No'))">
                <div v-if="teamDetail[0][0] !== 'No'" class="table-header">{{ teamDetail[0][1] }}</div>
                <div v-if="teamDetail[0][0] === 'No'" class="table-header">
                    <img src="../assets/images/filmCamera.svg" class="camera-style">
                </div>
                <div class="project-info-container">
                    <div class="button-container">
                        <a :href="teamDetail[3]" target="_blank" class="team-url-style">
                            <div class="project-header"> {{ teamDetail[1] }}</div>
                        </a>
                        <button v-if="windowWidth > 800 && challengeDetails === ''" class="challenges-button"
                            @click="toggleButton(teamDetail[3])">
                            <div class="button-text">
                                show challenges
                            </div>
                            <div class="image-container">
                                <img src="../assets/images/openChallengesArrow.svg" class="arrow-image-small"
                                    :class="{ 'arrow-right': !showChallenges.includes(teamDetail[3]), 'arrow-down': showChallenges.includes(teamDetail[3]) }"
                                    alt="Bitcamp sign" />
                            </div>
                        </button>
                        <button v-if="windowWidth < 800 && challengeDetails === ''" class="challenges-button-large"
                            @click="toggleButton(teamDetail[3])">
                            <img src="../assets/images/openChallengesArrowLarge.svg" class="arrow-image-large"
                                :class="{ 'arrow-right': !showChallenges.includes(teamDetail[1]), 'arrow-down': showChallenges.includes(teamDetail[1]) }"
                                alt="Bitcamp sign" />

                        </button>
                    </div>
                    <div v-if="teamDetail[2].length === 0"
                        :class="{ 'no-challenges-hidden': !showChallenges.includes(teamDetail[3]), 'no-challenges-shown': showChallenges.includes(teamDetail[3]) }">
                        No Challenges Selected
                    </div>
                    <div v-if="challengeDetails === ''"
                        :class="{ 'challenges-hidden': !showChallenges.includes(teamDetail[3]), 'challenges-shown': showChallenges.includes(teamDetail[3]) }">
                        <JudgingRow v-for="(challenge, challengeIndex) in teamDetail[2]"
                            :key="`challenge-${index}-${challengeIndex}`" :categoryName="challenge[0]"
                            :companyName="challenge[1]" :judgeName="challenge[2]" :timing="challenge[3]" />
                    </div>
                    <div v-if="challengeDetails !== ''" class="challenges-shown">
                        <JudgingRow
                            v-for="(challenge, challengeIndex) in teamDetail[2].filter(challenge => challengeDetails.includes(challenge[0]))"
                            :key="`challenge-${index}-${challengeIndex}`" :categoryName="challenge[0]"
                            :companyName="challenge[1]" :judgeName="challenge[2]" :timing="challenge[3]" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
    filtered: {
        type: Array,
        required: true,
    },
    teamDetails: {
        type: Array,
        required: true,
    },
    challengeDetails: {
        type: Array,
        required: true,
    },
    projectType: {
        type: Array,
        required: true,
    },
});

const sortedTeamDetails = computed(() => {
    if (props.challengeDetails !== "") {
        return [...props.teamDetails].sort((a, b) => {
            const aChallenge = a[2].find(challenge => props.challengeDetails.includes(challenge[0]));
            const bChallenge = b[2].find(challenge => props.challengeDetails.includes(challenge[0]));

            if (!aChallenge || !bChallenge) {
                return !aChallenge ? 1 : -1;
            }

            const timeToMinutes = time => {
                const [hours, minutes] = time.split(':').map(Number);
                return hours * 60 + minutes;
            };

            return timeToMinutes(aChallenge[3]) - timeToMinutes(bChallenge[3]);
        });
    }
    return props.teamDetails;
});

const showChallenges = ref<string[]>([]);
const windowWidth = ref(0);

const toggleStates = ref([]);

function toggleButton(link: string) {
    const index = showChallenges.value.indexOf(link);
    if (index !== -1) {
        showChallenges.value.splice(index, 1);
        toggleStates.value[index] = false;
    } else {
        showChallenges.value.push(link);
        var teamIndex = -1;
        var i = 0;
        while (i < 1) {
            if (props.teamDetails[i][3] === link) {
                teamIndex = i;
            }
            i = i + 1;
        }
        if (teamIndex !== -1) {
            toggleStates.value[teamIndex] = true;
        }
    }
}

const updateWindowWidth = () => {
    windowWidth.value = window.innerWidth;
};

onMounted(() => {
    updateWindowWidth();
    window.addEventListener('resize', updateWindowWidth);
    toggleStates.value = props.teamDetails.map(team => showChallenges.value.includes(team[3]));
});

onUnmounted(() => {
    window.removeEventListener('resize', updateWindowWidth);
});

watch([() => props.filtered, () => props.challengeDetails, () => props.projectType], () => {
    showChallenges.value = [];
}, { deep: true });
</script>
<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap');

.entire-container {
    background-color: #F6EBCC;
    border-radius: 2rem;
}

.top-row {
    display: flex;
    flex-direction: row;
    padding: 1rem 0 0;
    margin-inline: 1.25rem;

    @media (max-width: 800px) {
        display: inline-block;
        padding: 3rem 0 0 calc(10vw - 2.5rem);
    }
}

.project-info-container {

    display: flex;
    justify-content: space-between;
    flex-direction: column;
    position: relative;
    flex-grow: 1;
    color: #484241;

    @media (max-width: 800px) {
        align-items: center;
    }
}

.table-header {
    font-size: 1.5rem;
    width: 4rem;
    margin-right: 1.5rem;
    text-align: center;
    color: #FFC226;
    font-family: 'Aleo';
    min-width: 100px;
    display: flex;
    flex-wrap: wrap;
    align-content: flex-start;
    justify-content: center;

    @media (max-width: 800px) {
        background-color: #FF8F28;
        color: #FFFFFF;
        border-radius: 7%;
        height: 6rem;
        align-content: center;
        margin-inline: 24vw;
    }
}

.project-header {
    font-size: 1.5rem;
    color: #E34E30;
    font-family: 'Aleo';

    @media (max-width: 800px) {
        padding: 1.5rem 0.5rem 0;
    }
}

.challenges-button {
    padding: 0;
    margin: 0;
    border: none;
    background: none;
    text-align: left;
    padding-top: 0.5rem;
    display: flex;
    flex-direction: row;
    width: fit-content;
    font-family: 'Inter';
    color: #A49B83;
}

.challenges-button-large {
    padding: 0;
    margin: 0;
    border: none;
    background: none;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    flex-direction: row;
    width: fit-content;
    font-family: 'Inter';
    color: #FF8F28;
    padding-bottom: 0.3rem;
}

.challenges-hidden {
    display: none;
}

.no-challenges-hidden {
    display: none;
}

.challenges-shown {
    display: flex;
    flex-direction: column;
    width: 100%;
    font-family: 'Inter';

    @media (max-width: 800px) {
        padding-top: 1rem;
    }
}

.no-challenges-shown {
    display: flex;
    flex-direction: column;
    width: 100%;
    font-family: 'Inter';
    font-size: 0.75rem;
    font-weight: 600;
    padding-top: 1rem;

    @media (max-width: 800px) {
        text-align: center;
    }
}

.camera-style {
    width: 1.5rem;
}

.button-container {
    display: flex;
    flex-direction: column;

    @media (max-width: 800px) {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: flex-end;
    }
}

.toggle-size {
    transform: scale(0.8);
    transform-origin: center;
}

.image-container {
    display: flex;
}


.team-url-style {
    text-decoration: none;
    color: inherit;
}

.button-text {
    align-content: center;
    justify-content: space-evenly;
}

.arrow-image-small {
    margin-inline: 0.35rem;
    width: 0.69rem;
    transition: transform 0.3s ease;
}

.arrow-image-large {
    margin-inline: 0.35rem;
    width: 1rem;
    transition: transform 0.2s ease;
    color: #FF8F28;
}

.arrow-right {
    transform: rotate(0deg);
}

.arrow-down {
    transform: rotate(90deg);
}

.arrow-half {
    transform: rotate(45deg);
}
</style>