<template>
    <div class="wrapper">
        <div class="hero">
            <img src="../assets/images/background/HeroSign.svg" class="svgStyle" alt="Bitcamp sign" />
        </div>
        <div class="filter-and-competitions-content">
            <div class="filter-component">
                <FilterComponent :teamNames="state.teamNames" :challengeNames="state.categoryNames" />
            </div>
            <div class="competitions-component">
                <TeamContainer />
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { reactive, provide, onMounted } from 'vue';
import FilterComponent from "./FilterComponent.vue";
import TeamContainer from "./TeamContainer.vue";

const state = reactive({
    filteredTeamNames: [],
    filteredChallengeNames: "",
    projectType: "",
    challenges: [],
    categoryNames: [],
    teamNames: [],
});

const fetchData = async () => {
    const response = await fetch("/expo_algorithm_results.json");
    const data = await response.json();
    state.categoryNames = data.category_names;
    state.teamNames = data.combined_values.map((group) => group[1]);
};

onMounted(fetchData);

provide('state', state);
</script>

<style scoped lang="scss">
.hero {
    display: flex;
    justify-content: center;
    margin-bottom: 4rem;

    img {
        width: 30%;
        min-width: 20rem;
    }
}

.wrapper {
    position: absolute;
    background-image: linear-gradient(180deg, #7C3B35, #E26F3C, #F0984C);
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    padding: 4rem 0 6.5rem;

    @media (max-width: 800px) {
        padding: 3rem 0 5rem;
        height: 135vh;
    }
}

.filter-and-competitions-content {
    display: flex;
    flex-direction: row;
    justify-content: center;

    @media (max-width: 800px) {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-content: center;
        flex-wrap: wrap;
    }
}
</style>
