<template>
  <div class="entry">
    <div class="project-description">
      <div class="category-name">{{ categoryName }}</div>
      <!-- <div class="middle-char"></div> -->
    </div>
    <div class="judging-description" v-if="companyName !== 'MLH'">
      <div>{{ companyName }}</div>
      <div class="judging-description-inner">
        <div>{{ judgeName }}</div>
        <div class="middle-char">-</div>
        <!-- <div>{{ newTime }}</div> -->
        <div>{{ getFormattedTiming() }}</div>
      </div>
    </div>
    <div class="judging-description-mlh" v-if="companyName === 'MLH' ">
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
      if (!this.timing) return '';
      const timePart = this.timing.split(' ')[1];
      const [hours, minutes] = timePart.split(':');

      let hour = parseInt(hours);
      const amPm = hour >= 12 ? 'PM' : 'AM';
      hour = hour % 12;
      hour = hour ? hour : 12;

      return `${hour}:${minutes} ${amPm}`;
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
