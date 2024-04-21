<template>
  <div class="entire-container-filter">
    <div class="top-row">
      <div class="filter-header">Filter</div>
    </div>
    <div class="filters">
      <div class="filter-item">
        <div class="filter-title">Name</div>
        <input class="search-box" type="text" placeholder="Search..." @input="searchTeamNames($event)" />
      </div>
      <div class="filter-item">
        <div class="filter-title">Challenges</div>
        <select name="challenge" class="select-box" id="challenge" v-on:change="searchChallengeNames($event)">
          <option value="none">All Challenges</option>
          <option v-for="(name, index) in challengeNames" :key="index" :value="index">
            {{ name }}
          </option>
        </select>
      </div>
      <div class="filter-item">
        <div class="filter-title">Project Type</div>
        <select name="project-type" class="select-box" id="project-type" v-on:change="searchProjectType($event)">
          <option value="all">All Projects</option>
          <option value="in-person">In-Person Projects</option>
          <option value="virtual">Virtual Projects</option>
        </select>
      </div>
    </div>
    <div class="bottom-row"></div>
  </div>
</template>

<script>
import { inject, onMounted } from "vue";

export default {
  name: "FilterComponent",
  props: {
    challengeNames: {
      type: Array,
      required: true,
    },
    teamNames: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const state = inject("state");

    watch(() => props.teamNames, (newTeamNames) => {
      state.filteredTeamNames = newTeamNames;
    }, { immediate: true });

    onMounted(() => {
      state.filteredChallengeNames = '';
      state.projectType = 'all';
    });

    const searchTeamNames = (event) => {
      const searchTerm = event.target.value.toLowerCase();
      if (searchTerm === "") {
        state.filteredTeamNames = props.teamNames;
      } else {
        state.filteredTeamNames = props.teamNames.filter((name) =>
          name.toLowerCase().includes(searchTerm)
        );
      }
    };
    const searchChallengeNames = (event) => {
      const selectedChallengeIndex = event.target.value;
      const selectedChallenge =
        selectedChallengeIndex !== "none"
          ? props.challengeNames[selectedChallengeIndex]
          : "";
      if (!selectedChallenge || selectedChallenge == '') {
        state.filteredChallengeNames = "";
      } else {
        state.filteredChallengeNames = props.challengeNames
          .filter((name) => name.includes(selectedChallenge.split(' - ')[0]))
          .toString();
      }
    };
    const searchProjectType = (event) => {
      const selectedProjectTypeIndex = event.target.value;
      const selectedProjectType = selectedProjectTypeIndex;
      state.projectType = selectedProjectType;
    };
    return { searchTeamNames, searchChallengeNames, searchProjectType };
  },
};
</script>

<style scoped lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,100..900;1,100..900&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap");

.entire-container-filter {
  background-color: #f6ebcc;
  width: calc(5rem + 10vw);
  min-width: 10rem;
  height: 25.1rem;
  border-radius: 1.5rem;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1.5rem 3.3rem;
  margin-right: 1rem;
  overflow-x: hidden;

  @media (max-width: 800px) {
    width: calc(2rem + 65vw);
    margin: 0 2rem;
  }
}

.filter-header {
  font-family: "Aleo";
  color: #fa9747;
  font-weight: 400;
  font-size: 1.5rem;
}

.top-row {
  margin-bottom: 1.5rem;
}

.search-box {
  width: 100%;
  padding: 0.5rem;
  border-radius: 2rem;
  border: 2px solid #ff8e3f;
  background-color: #fff9ed;
  font-family: "Inter";
  margin-bottom: 1rem;
  padding-inline: 1rem;
  outline: none;
  box-sizing: border-box;
}

// to do make dropdown look nicer
.select-box {
  width: 100%;
  padding: 0.5rem;
  border-radius: 2rem;
  background-color: #ff8e3f;
  border: 2px solid #ff8e3f;
  font-family: "Inter";
  margin-bottom: 1rem;
  color: white;
  padding-inline: 1rem;
  border-right: 0.75rem solid transparent;
  cursor: pointer;
}

.filter-title {
  margin-bottom: 0.5rem;
  margin-left: 1rem;
  font-family: "Inter";
  font-weight: 300;
}

.filters {
  display: flex;
  width: 100%;
  flex-direction: column;
  align-items: flex-start;
}

.filter-item {
  margin-bottom: 1rem;
  width: 100%;
}

@media (max-width: 800px) {
  .search-box {
    width: calc(54% + 32vw);
  }

  .filter-item {
    margin-bottom: 0;
  }

  .filter-title {
    display: none;
    margin-bottom: 0;
  }

  .entire-container-filter {
    height: auto;
    padding-bottom: 1rem;
  }
}
</style>
