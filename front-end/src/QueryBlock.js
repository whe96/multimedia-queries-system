import React from "react";
import PropTypes from 'prop-types';

import './QueryBlock.css'

class QueryBlock extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            dropdownIsActive: false,
        };

        this.dropdownOnClick = this.dropdownOnClick.bind(this);
        this.updateCurrentQuery = this.updateCurrentQuery.bind(this);
        this.updateRatio = this.updateRatio.bind(this);
        this.queryButtonOnClick = this.queryButtonOnClick.bind(this);
    }

    dropdownOnClick() {
        this.setState({dropdownIsActive: !this.state.dropdownIsActive});
    }

    updateCurrentQuery(event) {
        event.preventDefault();
        this.setState({
            dropdownIsActive: !this.state.dropdownIsActive,
        });
        this.props.onQueryChange(event);
    }

    updateRatio(event) {
        this.props.onRatiosChange(event);
    }

    queryButtonOnClick() {
        this.props.onRequestData();
    }

    render() {
        let dropDownItems = this.props.folders.map((item) => {
            return (
                <a id={item} key={item} href="/" className={
                    "dropdown-item" + (this.props.currentQuery === item ? " is-active" : "")} onClick={this.updateCurrentQuery}>
                    {item}
                </a>);
        });

        let queryVideo = this.props.currentQuery !== '' ? (
            <video className="query-video-player" key={this.props.currentQuery}
                   width="480" height="360" controls autoPlay>
                <source
                    src={"http://localhost:5000/static/"+ this.props.currentQuery + ".mp4"}
                    type="video/mp4"
                />
            </video>) : null;

        return (
            <div className="query-block">
                <div className="query-block-left">
                    <div className={"dropdown" + (this.state.dropdownIsActive ? " is-active" : "")}>
                        <div className="dropdown-trigger" onClick={this.dropdownOnClick}>
                            <button className="button is-light dropdown-trigger-button"
                                    aria-haspopup="true" aria-controls="dropdown-menu">
                                <span>{this.props.currentQuery}</span>
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
                    {queryVideo}
                </div>
                <div className="query-block-right">
                    <label className="ratio-item">
                        <span className="ratio-label">Color ({this.props.ratios[0]})</span>
                        <input className="ratio-bar" type="range" name="color" min="0" max="5" step="1"
                               value={this.props.ratios[0]} onChange={this.updateRatio} />
                    </label>
                    <label className="ratio-item">
                        <span className="ratio-label">Motion ({this.props.ratios[1]})</span>
                        <input className="ratio-bar" type="range" name="motion" min="0" max="5" step="1"
                               value={this.props.ratios[1]} onChange={this.updateRatio} />
                    </label>
                    <label className="ratio-item">
                        <span className="ratio-label">Sound ({this.props.ratios[2]})</span>
                        <input className="ratio-bar" type="range" name="sound" min="0" max="5" step="1"
                               value={this.props.ratios[2]} onChange={this.updateRatio} />
                    </label>
                    <label className="ratio-item">
                        <span className="ratio-label">XXX ({this.props.ratios[3]})</span>
                        <input className="ratio-bar" type="range" name="xxx" min="0" max="5" step="1"
                               value={this.props.ratios[3]} onChange={this.updateRatio} />
                    </label>
                    <button className="button is-link query-button"
                            onClick={this.queryButtonOnClick}>Query
                    </button>
                </div>
            </div>
        );
    }
}

QueryBlock.propTypes = {
    folders: PropTypes.array,
    currentQuery: PropTypes.string,
    ratios: PropTypes.array,
    onQueryChange: PropTypes.func,
    onRatiosChange: PropTypes.func,
    onRequestData: PropTypes.func
};

export default QueryBlock;
