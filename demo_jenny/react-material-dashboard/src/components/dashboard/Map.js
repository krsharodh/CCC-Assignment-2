import React, { Component } from 'react';
import * as echarts from 'echarts';
import geoJson from './China';
import {
    Card,
    CardContent,
  } from '@material-ui/core';

class Map extends Component{
    constructor(props){
        super(props);
        this.state={
            data: []
        }
    }

    getSentimentScore() {
        fetch("http://127.0.0.1:5000/sentiment_score", {
            method: 'POST',
            headers: {
            "Content-Type": "application/x-www-form-urlencoded"
            },
            body: JSON.stringify({
            })
        }).then(res => res.json()).then(json => {
            this.state.data = json.data
            var myChart = echarts.init(document.getElementById('echartsmap'));
            let option={
                title: {
                    text: 'sentiment_score',
                },
                dataRange: {
                    x: 'left',
                    y: 'center',
                    splitList: [
                    {start: 500, label: '500 above', color:' rgb(200,50,100)'},
                    {start: 200, end: 500, label: '200-500', color: 'rgb(200,100,100)'},
                    {start: 50, end: 200, label: '50-200', color:' rgb(255,100,100)'},
                    {start: 10, end: 50, label: '10-50', color: 'rgb(255,255,100)'},
                    {start: 1, end: 10, label: '0-10', color:' rgb(255,255,200)'},
                    {start: 0, end: 1, label: '0', color:' rgb(255,255,255)'}
                    ]},
                tooltip: {},
                // toolbox: {
                //     show: true,
                //     orient: 'vertical',
                //     left: 'right',
                //     top: 'center',
                //     feature: {
                //         dataView: {readOnly: false},
                //         restore: {},
                //         saveAsImage: {}
                //     }
                // },
                series: [
                    {
                        name: 'sentiment_score',
                        type: 'map',
                        coordinateSystem: 'China',
                        map: 'China', // 自定义扩展图表类型
                        label: {
                            show: true
                        },
                        data: this.state.data,
                    }
                ]
            };
            myChart.setOption(option);
            myChart.hideLoading();
        })
    };

    componentWillMount(){
		this.getSentimentScore();
	}
    componentDidMount(){
        var myChart = echarts.init(document.getElementById('echartsmap'));
        echarts.registerMap('China', geoJson);
    }
    render() {
        return (
            <Card>
                <CardContent>
                <div id="echartsmap" style={{ width: 1500, height: 720}}></div>
                </CardContent>
            </Card>
        );
    }
}

export default Map;