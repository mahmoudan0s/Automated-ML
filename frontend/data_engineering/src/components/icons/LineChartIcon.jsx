const LineChartIcon = ({ size, ...props }) => (
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    viewBox="0 0 640 640" 
    fill="currentColor" 
    width={size} 
    height={size} 
    {...props}
  >
    <path d="M128 128c0-17.7-14.3-32-32-32s-32 14.3-32 32v336c0 44.2 35.8 80 80 80h400c17.7 0 32-14.3 32-32s-14.3-32-32-32H144c-8.8 0-16-7.2-16-16zm406.6 86.6c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L384 274.7l-57.4-57.3c-12.5-12.5-32.8-12.5-45.3 0l-96 96c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0l73.4-73.4 57.4 57.4c12.5 12.5 32.8 12.5 45.3 0l128-128z" />
  </svg>
);
export default LineChartIcon;
