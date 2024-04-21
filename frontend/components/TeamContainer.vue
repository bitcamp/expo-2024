<template>
  <div class="entire-container">
    <div class="no-submission-container"
      v-if="state.filteredTeamNames.length === 0 || filteredCombinedValues.length === 0">
      <div class="no-submission">No Submissions</div>
    </div>
    <!-- <div v-if="state.filteredTeamNames.length !== 0"> -->
    <div class="top-row" v-if="state.filteredTeamNames.length > 0 && filteredCombinedValues.length > 0">
      <div class="row-header-table"></div>
      <div class="row-header-project"></div>
      <div>{{ category_names }}</div>
    </div>
    <!-- <div class="content-row" v-if="state.filteredTeamNames.length > 0"> -->
    <div class="content-row"
      :class="{ 'content-row-hidden': state.filteredTeamNames.length === 0 || filteredCombinedValues.length === 0 }">
      <ProjectTeamInformation :filtered="state.filteredTeamNames" :challengeDetails="state.filteredChallengeNames"
        :projectType="state.projectType" :teamDetails="combinedValues" />
    </div>
    <!-- </div> -->
    <div class="bottom-row">
    </div>
  </div>
</template>

<script>
import { inject, computed } from "vue";
import ProjectTeamInformation from "./ProjectTeamInformation.vue";
export default {
  name: 'TeamContainer',
  setup() {
    const combinedValues = ref([]);
    const state = inject('state');
    const filteredCombinedValues = computed(() => {
      return combinedValues.value.filter(team => {
        let condition;
        if (state.projectType === 'in-person') {
          condition = team[0][0] === 'Yes';
        } else if (state.projectType === 'virtual') {
          condition = team[0][0] === 'No';
        } else {
          condition = team[0][0] === 'Yes' || team[0][0] === 'No';
        }

        let challengeCondition = true;
        if (state.filteredChallengeNames != '') {
          challengeCondition = team[2].some(challenge => challenge[0] === state.filteredChallengeNames.split(' - ')[0]);
        }

        let teamNameCondition = state.filteredTeamNames.includes(team[1]);

        return condition && challengeCondition && teamNameCondition;
      }).map(team => team[1]);
    });



    const fetchData = async () => {
      const response = await fetch("/expo_algorithm_results.json");
      const data = await response.json();
      combinedValues.value = data.combined_values.filter((entry) => {
        const title = entry[1];
        return title !== "Untitled";
      });
    };

    onMounted(() => {
      fetchData();
    });

    watch(() => state.filteredTeamNames, (newValue) => {
    }, { immediate: true });

    return { state, combinedValues, filteredCombinedValues };

  },
};
</script>

<style scoped lang="scss">
.entire-container {
  background-color: #F6EBCC;
  border-radius: 1.5rem;
  width: calc(20rem + 30vw);
  height: 30rem;

  @media (max-width: 800px) {
    width: calc(5rem + 65vw);
    height: 25rem;
    margin: 2rem auto;
  }

  .no-submission-container {
    height: 100%;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    .no-submission {
      color: #FFFF;
      font-family: "Aleo";
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      font-size: 2rem;
      border-radius: 1.5rem;
      padding: 10rem;
      background-color: #FF8F28;
      margin: auto;
      padding: 5rem;
      height: calc(4rem + 17.5vh);
      width: calc(4rem + 30vw);

      @media (max-width: 800px) {
        font-size: 1.4em;
        height: calc(4rem + 9.5vh);
        width: calc(4rem + 20vw);
      }
    }
  }
}

.top-row {
  height: fit-content;
  display: flex;
  flex-direction: row;
  margin-inline: 1.25rem;
  padding: 1rem 0 0;
  padding-bottom: 0.5rem;
  border-bottom-color: #FF8F28;
  border-bottom-width: 0.069rem;
  border-bottom-style: solid;
}

.row-header-table {
  font-size: 1.5rem;
  width: 6rem;
  margin-right: 1.5rem;
  text-align: center;
  color: #FF8F28;
  font-family: 'Aleo';
  min-width: 100px;

  @media screen and (max-width: 800px) {
    margin-right: 0;
  }
}

.row-header-project {
  font-size: 1.5rem;
  color: #FF8F28;
  font-family: 'Aleo';

  @media screen and (max-width: 800px) {
    margin: auto;
  }
}


.row-header-table::before {
  content: "Table";
}

.row-header-project::before {
  content: "Project";
}

@media screen and (max-width: 800px) {
  .row-header-table {
    display: none;
  }

  .row-header-project::before {
    content: "Project Information";
  }
}

.content-row {
  overflow-x: hidden;
  overflow-y: auto;
  max-height: 81%;
  // height: 30rem;
}

.content-row-hidden {
  display: none;
  height: 0;
  overflow: hidden;
}

.no-submission-active .row-header-project::before {
  content: "";
}
</style>
