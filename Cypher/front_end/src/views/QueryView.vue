<template>
  <div class="introview-container">
    <h1 class="h3 mt-4">项目简介</h1>
    <hr />
    <div class="mt-4 pl-2 content">
      <p>
        <strong>陈奕迅歌曲知识图谱问答系统</strong>
      </p>
      <p>
        本项目爬取线上陈奕迅相关的歌曲信息，为每一首歌曲定义歌手、作词人、作曲人、专辑和发行时间的相关信息，并构建知识图谱。问答系统基于知识图谱进行查询并给出查询结果。
      </p>
      <p>
        系统共定义了8种交互模式，通过输入语句匹配对应的模式，并到neo4j数据库中进行查询，最终返回查询结果。
      </p>
      <p>Tips: 参考提问模板进行提问哦！</p>
    </div>
  </div>

  <div class="queryview-container">
    <h1 class="h3 mt-4">图谱问答</h1>
    <hr />
    <div class="mt-4 row justify-content-center">
      <form class="col-10">
        <div class="row mb-3 justify-content-center">
          <label class="col-auto col-form-label" for="inputGroupSelect01">参考模版</label>
          <select class="col-10" id="inputGroupSelect01">
            <option selected>提问模版</option>
            <option v-for="(item, index) in templates" :key="index" value="item.index">
              {{ item }}
            </option>
          </select>
        </div>

        <div class="row mb-3 justify-content-center">
          <label class="col-auto col-form-label" for="question">查询问句</label>
          <input
            type="text"
            class="col-10"
            id="question"
            v-model="query"
            placeholder="请参照模版输入查询问句"
          />
        </div>

        <div class="text-center">
          <button type="button" class="btn btn-primary" @click.prevent="toQuery">查询</button>
        </div>
        <hr />
      </form>
      <div class="col-10">
        <p class="answer" id="answer" :style="{ color: color }">
          {{ queryResult }}
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      templates: [
        '歌曲相信你的人所属的专辑是',
        '歌曲相信你的人的作词人是',
        '歌曲相信你的人的作曲人是',
        '歌曲相信你的人的歌手是',
        '专辑L.O.V.E.包含的歌曲有',
        '陈奕迅演唱的歌曲有',
        '林家谦作曲的歌曲有',
        '小克作词的歌曲有',
      ],
      query: '',
      queryResult: '',
      color: 'black'
    }
  },
  methods: {
    async sendQuery() {
      const { data: res } = await this.$http.post('/api/query', {
        question: this.query.trim()
      })
      this.queryResult = res.msg
      if (res.state === 0) {
        res.data.forEach((item, index) => {
          index === 0 ? (this.queryResult += '：' + item) : (this.queryResult += '、' + item)
        })
        this.color = 'green'
        return
      }
      this.color = 'red'
    },
    toQuery() {
      let trim = this.query.trim()
      if (!trim) {
        this.queryResult = '查询语句不能为空，请重新输入！'
        this.color = 'red'
        this.query = ''
        return
      }
      this.queryResult = '正在查询...'
      this.color = 'black'
      this.sendQuery()
    }
  }
}
</script>

<style lang="less" scoped>
select {
  color: #666;
}

.answer {
  padding-top: 20px;
  text-align: center;
  font-weight: bold;
}
</style>
