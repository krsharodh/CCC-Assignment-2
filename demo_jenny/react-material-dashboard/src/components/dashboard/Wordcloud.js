import ReactWordcloud from 'react-wordcloud';
import React, { Component } from 'react';
import {
  Card,
  CardContent,
} from '@material-ui/core';

import "tippy.js/dist/tippy.css";
import "tippy.js/animations/scale.css";

const options = {
  colors: ['#1f77b4', '#ff7f0e', "#2ca02c", "#d62728", "#9467bd", "#8c564b"],
  deterministic: false,
  fontFamily: "Times New Roman",
  fontSizes: [15, 100],
  fontStyle: "normal",
  fontWeight: "normal",
  padding: 1,
  rotations: 1,
  rotationAngles: [0, 90],
  scale: "log",
  spiral: "archimedean",
  transitionDuration: 1000
};

const size = [1000, 600];

class WordCloud extends Component{
    constructor(props){
        super(props);
        this.state={
            data: []
        }
    }

    getWordCloud() {
        fetch("http://127.0.0.1:5000/words_cloud", {
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
                <Card>
                    <CardContent>
                        <div>
                            <span>Word Cloud of Top frequent words</span>
                        </div>
                        <ReactWordcloud words={this.state.data} options={options} size={size} />
                    </CardContent>
                </Card>
        );
    }
}

export default WordCloud;
