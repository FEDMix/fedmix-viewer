import * as cv from 'opencv.js'

export default (context, inject) => {
  inject('cv', cv)
  context.$cv = cv
}
