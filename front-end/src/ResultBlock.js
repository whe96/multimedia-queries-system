import React from "react";
import PropTypes from "prop-types";

import Chart from 'chart.js'

import './ResultBlock.css'

class ResultBlock extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            dropdownIsActive: false,
            result: this.props.resultData[0]['dir'],
        };

        this.dropdownOnClick = this.dropdownOnClick.bind(this);
        this.updateCurrentResult = this.updateCurrentResult.bind(this);
    }

    componentDidMount() {
        this.interval = setInterval(() => this.setState({ time: Date.now() }), 100);
        this.drawAreaChart();
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.state.result !== prevState.result) {
            this.drawAreaChart();
        }
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    drawAreaChart() {
        let d = this.props.resultData.filter((item) => (item['dir'] === this.state.result))[0];

        if (this.areaChart) {
            this.areaChart.destroy();
        }

        this.areaChart = new Chart(this.areaChartRef, {
            type: 'line',
            data: {
                labels: Array.from({length: 200}, (v, k) => k+1),
                datasets: [{
                    data: d['data'],
                    label: 'Similarity Score (10 fps)',
                    fill: 'start'
                }],
            },
            options:{
                scales: {
                    xAxes: [{
                        display: false
                    }]
                },
                legend: {
                    onClick: (e) => e.stopPropagation()
                }
            },
        });
    }

    dropdownOnClick() {
        this.setState({dropdownIsActive: !this.state.dropdownIsActive});
    }

    updateCurrentResult(event) {
        event.preventDefault();
        this.setState({
            dropdownIsActive: !this.state.dropdownIsActive,
            result: event.target.id
        });
    }

    render() {
        let d = this.props.resultData.filter((item) => (item['dir'] === this.state.result))[0];

        let dropDownItems = this.props.resultData.map((item) => {
            return (
                <a id={item['dir']} key={item['dir']} href="/" className={
                    "dropdown-item" + (this.state.result === item['dir'] ? " is-active" : "")}
                   onClick={this.updateCurrentResult}>
                    {item['dir'] + ' (' + (item['score']) + ')'}
                </a>);
        });

        let resultVideo = (
            <video ref={(v) => (this.resultVideo = v)}
                className="query-video-player" key={this.state.result}
               width="480" height="360" controls autoPlay>
                <source
                    src={"http://localhost:5000/static/"+ this.state.result + ".mp4"}
                    type="video/mp4"
                />
            </video>);

        let currentProgress = (this.resultVideo && !isNaN((this.resultVideo.currentTime / this.resultVideo.duration))) ?
            (this.resultVideo.currentTime / this.resultVideo.duration) : 0;

        return (
            <div className="result-block">
                <div className="result-block-left">
                    <div className={"dropdown" + (this.state.dropdownIsActive ? " is-active" : "")}>
                        <div className="dropdown-trigger" onClick={this.dropdownOnClick}>
                            <button className="button is-light dropdown-trigger-button"
                                    aria-haspopup="true" aria-controls="dropdown-menu">
                                <span>{d['dir'] + ' (' + (d['score']) + ')'}</span>
                                <span className="icon is-small dropdown-trigger-icon">
                                    <i className="fas fa-angle-down" aria-hidden="true" />
                                </span>
                            </button>
                        </div>
                        <div className="dropdown-menu" id="dropdown-menu" role="menu">
                            <div className="dropdown-content">
                                {dropDownItems}
                            </div>
                        </div>
                    </div>
                    {resultVideo}
                </div>
                <div className="result-block-right">
                    <div className="result-block-chart">
                        <canvas className="result-block-canvas" ref={(myRef) => this.areaChartRef = myRef} />
                    </div>
                    <div>
                        <progress className="progress is-link progress-bar"
                                  value={currentProgress} max="1"
                        />
                    </div>
                </div>
            </div>
        );
    }
}

ResultBlock.propTypes = {
    resultData: PropTypes.array
};

export default ResultBlock;
