import React, { Component } from 'react';
import {
  ComposedChart,
  Line,
  Area,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  Scatter,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';



const data = [
];

class VaccineTrend extends Component {
    constructor(props){
        super(props);
        this.state={
            data: [
                {
                    'date': '2020-02-01',
                    'l': -0.5,
                    'u': 0.5,
                    'value': 0.2
                },
                {
                    'date': '2020-02-02',
                    'l': -0.3,
                    'u': 0.6,
                    'value': 0.1
                },
                {
                    'date': '2020-02-03',
                    'l': -0.5,
                    'u': 0.6,
                    'value': 0.4
                },
                {
                    'date': '2020-02-04',
                    'l': -0.2,
                    'u': 0.5,
                    'value': 0.3
                },
                {
                    'date': '2020-02-05',
                    'l': -0.5,
                    'u': 0.5,
                    'value': 0.2
                }
            ]
        }
    }

    getSentimentTrend() {
        fetch("http://127.0.0.1:5000/vaccine/sentiment_trend", {
            method: 'POST',
            headers: {
            "Content-Type": "application/x-www-form-urlencoded"
            },
            body: JSON.stringify({
            })
        }).then(res => res.json()).then(json => {
            this.state.data = json.data
            this.setState({data: json.data})
            console.log(this.state.data)
        })
    };

    componentWillMount(){
		this.getSentimentTrend();
	}

    render() {
        return (
            <div>
                <p style={{'text-align': "center",'font-size':'22px',"margin-top":'20px'}}>Sentiment Score of Vaccine-Related Tweets Over Time</p>
                <ComposedChart
                    width={1200}
                    height={600}
                    data={this.state.data}
                    margin={{
                        top: 20,
                        right: 20,
                        bottom: 20,
                        left: 20,
                    }}
                    >
                    <CartesianGrid stroke="#f5f5f5" />
                    <XAxis dataKey="date" interval={5}/>
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" name="80% confidence band" dataKey="range" fill="#8884d8" stroke="#8884d8" fillOpacity={0.3} strokeOpacity={0.5}/>
                    <ReferenceLine y={0}  stroke="red" stroke="#040404" strokeDasharray="5 5" />
                    <Line type="monotone" name="avg_sentiment_score" dataKey="value" stroke="#8884d8" strokeWidth={3} />
                    </ComposedChart>
            </div>
        );
    } 
}

export default VaccineTrend;