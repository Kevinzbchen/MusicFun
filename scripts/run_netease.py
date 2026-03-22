"""
Main runner script for Netease Music crawler.
All output in English, ASCII only.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
import argparse
from loguru import logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.platforms.netease.crawler import NeteaseCrawlerFixed as NeteaseCrawler
from src.core.logger import setup_logger
from config.settings import LOG_DIR


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Netease Music Crawler")
    parser.add_argument("--keyword", "-k", default="mihoyo", help="Search keyword (default: mihoyo)")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max songs to process (default: 10)")
    parser.add_argument("--output", "-o", default=None, help="Output filename (default: auto-generated)")
    parser.add_argument("--comments-per-song", "-c", type=int, default=10, help="Max comments per song (default: 10)")
    parser.add_argument("--mock-only", "-m", action="store_true", help="Use mock data only (no real API calls)")

    args = parser.parse_args()
    
    # Setup logger
    setup_logger(log_level="INFO", log_dir=LOG_DIR)
    
    logger.info("=" * 50)
    logger.info("Netease Music Crawler Started")
    logger.info(f"Keyword: {args.keyword}")
    logger.info(f"Max songs: {args.limit}")
    logger.info(f"Comments per song: {args.comments_per_song}")
    logger.info(f"Mock mode: {args.mock_only}")
    logger.info("=" * 50)
    
    try:
        # Create crawler instance
        crawler = NeteaseCrawler(use_mock=args.mock_only)

        # Override max comments per song in config
        crawler.config["max_comments_per_song"] = args.comments_per_song
        
        # Run crawler
        logger.info("Starting search and comment extraction...")
        results = crawler.search_and_get_comments(args.keyword, max_songs=args.limit)
        
        if not results:
            logger.warning("No results found")
            return
        
        # Prepare output filename
        if args.output:
            output_file = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            mock_suffix = "_mock" if args.mock_only else ""
            output_file = f"netease_{args.keyword}_{timestamp}{mock_suffix}.json"

        # Save results
        output_path = Path("data/processed") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        logger.info("=" * 50)
        logger.info(f"SUCCESS! Processed {len(results)} songs")
        logger.info(f"Output saved to: {output_path}")
        logger.info("=" * 50)
        
        # Print summary
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        for idx, (song_name, data) in enumerate(results.items(), 1):
            comment_count = len(data.get("hot_comments", []))
            print(f"{idx}. {song_name} - {comment_count} hot comments")
        print("=" * 50)
        
        # Close crawler
        crawler.close()
        
    except KeyboardInterrupt:
        logger.info("Crawler interrupted by user")
    except Exception as e:
        logger.error(f"Crawler failed: {e}")
        raise


if __name__ == "__main__":
    main()
