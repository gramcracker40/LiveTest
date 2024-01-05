import React from 'react';

const About = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 text-white px-6 py-24 text-center shadow-2xl">
      <div className="max-w-2xl">
        <h1 className="text-4xl font-bold mb-6 text-cyan-500">About LiveTest</h1>
        <p className="mb-8 text-gray-300">
          LiveTest is a cutting-edge software solution designed to streamline the process of submitting and grading answer sheets. Our platform aims to revolutionize traditional testing methods, providing a seamless experience for both educators and students.
        </p>
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold mb-2 text-cyan-500">Key Features:</h2>
          <ul className="list-disc list-inside mb-6 text-gray-300">
            <li className="mb-2">Effortless Answer Sheet Submission: Students can easily submit their answer sheets through our user-friendly interface, eliminating the need for manual collection.</li>
            <li className="mb-2">Automated Grading System: LiveTest employs advanced algorithms to automatically grade answer sheets, saving educators valuable time and ensuring accuracy.</li>
            <li className="mb-2">Comprehensive Analytics Section: Gain deep insights into test performance with our analytics section, providing detailed statistics and visualizations for each test.</li>
            <li>Customizable Tests: Educators can create and customize tests based on their curriculum, tailoring assessments to meet specific educational objectives.</li>
          </ul>
        </div>
        <div className="space-y-4">
          <h2 className="text-2xl font-semibold mb-2 text-cyan-500">Analytics Features:</h2>
          <p className="mb-4 text-gray-300">
            Our comprehensive analytics section goes beyond simple grading, offering educators valuable data to enhance teaching strategies and student understanding. Key analytics features include:
          </p>
          <ul className="list-disc list-inside mb-6 text-gray-300">
            <li className="mb-2">Individual Student Performance: View detailed performance metrics for each student, identifying strengths and areas for improvement.</li>
            <li className="mb-2">Classwide Trends: Analyze overall class performance trends to identify topics that may require additional focus during instruction.</li>
            <li>Question-Level Analytics: Drill down into the performance of specific questions to assess the effectiveness of test questions and adjust future assessments accordingly.</li>
          </ul>
        </div>
        <p className="text-gray-300">
          LiveTest is committed to simplifying the testing and grading process while providing educators with powerful tools to optimize their teaching strategies. Join us in transforming the way assessments are conducted and analyzed.
        </p>
      </div>
    </div>
  );
};

export default About;
