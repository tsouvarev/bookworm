new Vue({
  el: "#app",
  data: {
    books: [],
    isLoading: true,
    new_book: {},
    new_book_errors: {},
    show_add_form: false,
  },
  delimiters: ["[[", "]]"],
  mounted() {
    axios.get('/books/').then(response => {
      this.books = response.data;
      this.isLoading = false;
    });
  },
  methods: {
    create_book: function () {
      axios.post(`/books/`, this.new_book).then(response => {
        this.books.unshift(response.data);
        this.new_book_errors = {};
      }).catch(error => {
        this.new_book_errors = error.response.data.errors;
      })
    },
    delete_book: function (book_id) {
      axios.delete(`/books/${book_id}/`).then(response => {
        this.books = this.books.filter(value => value.id != book_id);
      })
    }
  }
});

let csrf_meta_tag = document.querySelector('meta[name="csrf-token"]');
let csrf_token = csrf_meta_tag.getAttribute('content');
axios.defaults.headers.common['X-CSRF-TOKEN'] = csrf_token;
