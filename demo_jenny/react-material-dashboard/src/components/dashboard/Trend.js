import React, { Component } from 'react';
import * as echarts from 'echarts';
import {
    Card,
    CardContent,
  } from '@material-ui/core';

class Trend extends Component{
    constructor(props){
        super(props);
        this.state={
            data: []
        }
    }

    getSentimentTrend() {
        fetch("http://127.0.0.1:5000/sentiment_trend", {
            method: 'POST',
            headers: {
            "Content-Type": "application/x-www-form-urlencoded"
            },
            body: JSON.stringify({
            })
        }).then(res => res.json()).then(json => {
            this.state.data = json.data
            var myChart = echarts.init(document.getElementById('sentimentTrend'));
            let option={
                title: {
                    text: 'Sentiment Score Trend',
                    left: 'center'
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        animation: false,
                        label: {
                            backgroundColor: '#ccc',
                            borderColor: '#aaa',
                            borderWidth: 1,
                            shadowBlur: 0,
                            shadowOffsetX: 0,
                            shadowOffsetY: 0,
        
                            color: '#222'
                        }
                    },
                    formatter: function (params) {
                        return params[2].name + '<br />' + (params[2].value);
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: this.state.data.map(function (item) {
                        return item.date;
                    }),
                    axisLabel: {
                        formatter: function (value, idx) {
                            var date = new Date(value);
                            return idx === 0 ? value : [date.getMonth() + 1, date.getDate()].join('-');
                        }
                    },
                    boundaryGap: false
                },
                yAxis: {
                    axisLabel: {
                        formatter: function (val) {
                            return val;
                        }
                    },
                    axisPointer: {
                        label: {
                            formatter: function (params) {
                                return params.value;
                            }
                        }
                    },
                    splitNumber: 3
                },
                series: [{
                    name: 'L',
                    type: 'line',
                    data: this.state.data.map(function (item) {
                        return item.l;
                    }),
                    lineStyle: {
                        opacity: 0
                    },
                    areaStyle: {
                        color: 'pink'
                    },
                    stack: 'confidence-band',
                    symbol: 'none'
                }, {
                    name: 'U',
                    type: 'line',
                    data: this.state.data.map(function (item) {
                        return item.u;
                    }),
                    lineStyle: {
                        opacity: 0
                    },
                    areaStyle: {
                        color: 'pink'
                    },
                    stack: 'confidence-band',
                    symbol: 'none'
                }, {
                    type: 'line',
                    data: this.state.data.map(function (item) {
                        return item.value;
                    }),
                    hoverAnimation: false,
                    symbolSize: 6,
                    itemStyle: {
                        color: '#333'
                    },
                    showSymbol: false
                }]
            };
            myChart.setOption(option);
            myChart.hideLoading();
        })
    };

    componentWillMount(){
		this.getSentimentTrend();
	}
    componentDidMount(){
    }
    render() {
        return (
            <Card>
                <CardContent>
                <div id="sentimentTrend" style={{ width: 1200, height: 720}}></div>
                </CardContent>
            </Card>
        );
    }
}

export default Trend;