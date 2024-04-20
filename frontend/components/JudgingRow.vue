<template>
  <div class="entry">
    <div class="project-description">
      <div class="category-name">{{ categoryName }}</div>
      <!-- <div class="middle-char"></div> -->
    </div>
    <div class="judging-description" v-if="companyName !== 'Major League Hacking'">
      <div>{{ companyName }}</div>
      <div class="judging-description-inner">
        <div>{{ judgeName }}</div>
        <div class="middle-char">-</div>
        <!-- <div>{{ newTime }}</div> -->
        <div>{{ getFormattedTiming() }}</div>
      </div>
    </div>
    <div class="judging-description-mlh" v-if="companyName === 'Major League Hacking'">
      <div>{{ companyName }}</div>
      <div>Consult MLH</div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'JudgingRow',
  props: {
    categoryName: {
      type: String,
      required: true,
    },
    companyName: {
      type: String,
      required: true,
    },
    judgeName: {
      type: String,
      required: true,
    },
    timing: {
      type: String,
      required: true,
    },
  },
  methods: {
    getFormattedTiming() {
      let time = this.timing;
      if (time.startsWith("0")) {
        time = time.substring(1);
      }
      const hour = parseInt(time.split(':')[0]);
      if (hour < 12) {
        time += " AM";
      }
      else {
        time += " PM";
      }
      return time;
    }
  },
};
</script>

<style scoped lang="scss">
.entry {
  background-color: #f8eccc;
  width: 96%;
  padding-top: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  .project-description {
    display: flex;
    font-size: 0.75rem;
    font-weight: 400;
    padding-right: 2rem;

    @media (max-width: 800px) {
      display: inline-block !important;
    }

    .category-name {
      font-weight: 600;
    }

    .middle-char::before {
      content: "|";
    }

    @media screen and (max-width: 800px) {
      .middle-char {
        display: none;
      }
    }
  }

  .judging-description {
    display: flex;
    justify-content: space-between;
    flex-wrap: nowrap;
    font-size: 0.75rem;
    font-weight: 400;
  }

  .judging-description-inner {
    display: flex;
    flex-direction: row;
  }

  .judging-description-mlh {
    display: flex;
    font-size: 0.75rem;
    font-weight: 400;
    justify-content: space-between;
  }
}

.middle-char {
  margin-inline: 0.5rem;
}
</style>
