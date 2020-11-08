import './App.css';
import axios from 'axios';

import React,{Component} from 'react';

class App extends Component{
  constructor (){
    super();
  }
  
  state = {
    slectedFile: null
  };

  onFileChange = event => {
    this.setState({ selectedFile: event.target.files[0]});
  };

  onFileUpload = () => {
    const formData = new FormData();
    formData.append(
      "myFile",
      this.state.selectedFile,
      this.state.selectedFile.name
    );
    console.log(this.state.selectedFile);
    axios.post("api/uploadfile, formData");
  };
  fileData = () => {
    if (this.state.selectedFile){
      return (
        <div>
          <h2>File Details:</h2>
          <p>File Name: {this.state.selectedFile.name}</p>
          <p>File Type: {this.state.selectedFile.type}</p>
      <p>Last Modified:{" "}{this.state.selectedFile.lastModifiedDate.toDateString()}</p>
        </div>
      );
    }else{
      return (
        <div>
          <br />
          <h4 style={this.getStyle3()}>Choose file, then click upload</h4>
        </div>
      );
    };
    
  }

  render (){
    return (
      <div>
        <h1 style={this.getStyle1()}>Quiz Creator</h1>
        <h3 style={this.getStyle2()}>Upload Notes Here</h3>
        <div style={this.getStyle2()}>
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>
            Upload
          </button>
        </div>
        {this.fileData()}
        <h3 style={this.getStyle1()}>Search Quizzes Here</h3>
        <div className="App"></div>
           <span className="Controls">
             <button><strong>Search</strong></button>
           </span>
           <textarea rows="5" className="Text" />
      </div>
    );
  };

  getStyle1 = () => {
    return {
        background: '#003366',
        color: '#ffffff',
        padding: '50px',
        borderTop: '1px #ccc dotted',
        borderBottom: '1px #ccc dotted',
        fontFamily: 'Arial',
        textAlign: 'center'
    }
  }
  getStyle2 = () => {
    return {
        padding: '10px',
        fontFamily: 'Arial',
        textAlign: 'center'
    }
  }
  getStyle3 = () => {
    return {
      background: '#003366',
      color: '#ffffff',
      padding: '10px',
      fontFamily: 'Arial',
      textAlign: 'center'
    }
  }
}
export default App;