import React, { useState } from 'react';
import {Container, Content, Section, Sidebar, Title} from './styles';
import Cookies from './subpages/cookies';
import SearchEngine from './subpages/searchEngine';
import Appearance from './subpages/appearance';
import Downloads from './subpages/downloads';

const Settings = () => {
    const [activeSection, setActiveSection] = useState('cookies');

    const sections = {
      cookies: "Cookies",
      searchEngine: "Search Engine",
      appearance: "Appearance",
      downloads: "Downloads",
    };

    const renderContent = () => {
      switch (activeSection) {
        case 'cookies':
          return <Cookies></Cookies>;
        case 'searchEngine':
          return <SearchEngine></SearchEngine>;
        case 'appearance':
          return <Appearance></Appearance>;
        case 'downloads':
          return <Downloads></Downloads>;
        default:
          return <p>Select a setting</p>;
      }
    };
  
    return (
      <Container>
        <Sidebar>
          {Object.keys(sections).map(key => (
            <Section key={key} onClick={() => {
                setActiveSection(key);
            }}>
              {sections[key]}
            </Section>
          ))}
        </Sidebar>
        <Content>
          <Title>{sections[activeSection]}</Title>
          {renderContent()}
        </Content>
      </Container>
    );
};

export default Settings;
