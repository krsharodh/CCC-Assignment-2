import ReactWordcloud from 'react-wordcloud';
import React, { Component } from 'react';
import { select } from "d3-selection";
import {
  Card,
  CardContent,
} from '@material-ui/core';

import "tippy.js/dist/tippy.css"
import "tippy.js/animations/scale.css";

const options = {
  colors: ['#1f77b4', '#ff7f0e', "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
  deterministic: false,
  fontFamily: "Times New Roman",
  fontSizes: [15, 80],
  fontStyle: "normal",
  fontWeight: "normal",
  padding: 1,
  rotations: 1,
  rotationAngles: [0, 90],
  scale: "log",
  spiral: "archimedean",
  transitionDuration: 1000,
  tooltipOptions: {
    allowHTML: true,
    appendTo: document.body,
    interactive: true,
    hideOnClick: false,
  }
};

const size = [1000, 600];
function getCallback(callback) {
    return function (word, event) {
        const isActive = callback !== "onWordMouseOut";
        const element = event.target;
        const text = select(element);
        text
        .transition()
        .attr("font-size", isActive ? word.size * 1.2 + 'px' : word.size + 'px')
        if (callback === 'onWordClick') {
            fetch("http://127.0.0.1:5000/covid/hashtag/get_tweet_by_word", {
            method: 'POST',
            headers: {
            "Content-Type": "application/json"
            },
            body: JSON.stringify({'word':word.text
            })
            }).then(res => res.json()).then(json => {
                var element = document.getElementById(word.text)
                var startIndex = json.data.toLowerCase().indexOf(word.text)
                var endIndex = startIndex + word.text.length
                if (element !== null) {
                    var innerHtml = ""
                    if (startIndex === 0) {
                        innerHtml = innerHtml + "<text><text style='color:#ff8000'>" + json.data.slice(0,endIndex) + "</text>" + json.data.slice(endIndex,json.data.length) + "</text>"
                    } else if (startIndex === -1) {
                        innerHtml = "<text>" + json.data + "</text>"
                    } else {
                        innerHtml = innerHtml + "<text>" + json.data.slice(0,startIndex) + "<text style='color: #ff8000'>" + json.data.slice(startIndex,endIndex) + "</text>" +json.data.slice(endIndex,json.data.length) + "</text>"
                    }
                    element.innerHTML = innerHtml
                }
                var content = document.getElementById(word.text + '_1')
                if (content !== null) {
                    content.innerText = 'Example tweet with "' + word.text + '": '
                }
            })
        }
    };
  }
const callbacks = {
    getWordTooltip: (word) =>
      `<p id='${word.text + "_1"}'>The hashtag "${word.text}" appears ${word.value} times.</p>
      <div id='${word.text}'></div>`,
    onWordClick: getCallback('onWordClick'),
    onWordMouseOut: getCallback("onWordMouseOut"),
    onWordMouseOver: getCallback('onMouseOver')
  };


class WordCloudCovidHashTag extends Component{
    constructor(props){
        super(props);
        this.state={
            data: []
        }
    }

    getWordCloud() {
        fetch("http://127.0.0.1:5000/covid/hashtag/words_cloud", {
            method: 'POST',
            headers: {
            "Content-Type": "application/x-www-form-urlencoded"
            },
            body: JSON.stringify({
            })
        }).then(res => res.json()).then(json => {
            this.setState({data: json.data})
            console.log(this.state)
        })
    };

    componentWillMount(){
		this.getWordCloud();
	}

    render() {
        return (
            <div>
                <span>Word Cloud of Top frequent covid-related hashtags</span>
                <ReactWordcloud callbacks={callbacks} words={this.state.data} options={options} size={size} />
            </div>
        );
    }
}

export default WordCloudCovidHashTag;
