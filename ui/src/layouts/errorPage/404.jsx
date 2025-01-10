import React from 'react'
import { FaRegArrowAltCircleLeft } from 'react-icons/fa'
import Button from "src/components/Button/Button"
import style from './error.module.css'
import DashboardBody from 'src/layouts/dashboard/DashboadBody'
import { useNavigate } from 'react-router-dom'
import { v4 } from "uuid"
import errorImage from '../../assets/images/404.svg'

const NotFound = () => {
    const navigate = useNavigate()
    return (
        <DashboardBody title="">
            <div className={style.error}>
                <img src={errorImage}></img>
                {/* <svg width="350" height="136" viewBox="0 0 350 136" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M0 109.235V87.5278L54.4264 1.78239H73.1414V31.8283H62.0652L27.7543 86.1274V87.1459H105.097V109.235H0ZM62.5745 132.151V102.614L63.0837 93.0023V1.78239H88.9283V132.151H62.5745Z" fill="#E6F2FF" />
                    <path d="M174.578 135.016C163.629 134.973 154.208 132.278 146.315 126.931C138.464 121.584 132.416 113.839 128.173 103.697C123.971 93.554 121.892 81.3532 121.934 67.0941C121.934 52.8774 124.035 40.7615 128.236 30.7461C132.48 20.7308 138.527 13.1133 146.378 7.89343C154.272 2.63114 163.672 0 174.578 0C185.485 0 194.863 2.63114 202.714 7.89343C210.608 13.1557 216.676 20.7945 220.92 30.8098C225.164 40.7827 227.265 52.8774 227.222 67.0941C227.222 81.3956 225.1 93.6177 220.857 103.76C216.655 113.903 210.629 121.648 202.778 126.995C194.927 132.342 185.527 135.016 174.578 135.016ZM174.578 112.163C182.047 112.163 188.01 108.407 192.466 100.896C196.922 93.3843 199.128 82.117 199.086 67.0941C199.086 57.2061 198.068 48.9732 196.031 42.3953C194.036 35.8175 191.193 30.8735 187.501 27.5633C183.851 24.2532 179.543 22.5981 174.578 22.5981C167.152 22.5981 161.21 26.3114 156.754 33.738C152.298 41.1646 150.049 52.2833 150.007 67.0941C150.007 77.1094 151.004 85.4696 152.999 92.1748C155.036 98.8375 157.9 103.845 161.592 107.198C165.284 110.508 169.613 112.163 174.578 112.163Z" fill="#E6F2FF" />
                    <path d="M244.903 109.235V87.5278L299.329 1.78239H318.044V31.8283H306.968L272.657 86.1274V87.1459H350V109.235H244.903ZM307.477 132.151V102.614L307.987 93.0023V1.78239H333.831V132.151H307.477Z" fill="#E6F2FF" />
                </svg> */}
                <div className={style.errorText}>
                    <h3>So Sorry,</h3>
                    <p>We couldn’t find what were you looking for...</p>
                    <Button className={style.iconButton} onClick={() => navigate(`/preview/${v4()}/chat`)} ><FaRegArrowAltCircleLeft />Go Back</Button>
                </div>
            </div>
        </DashboardBody>
            );
  };

            export default NotFound;