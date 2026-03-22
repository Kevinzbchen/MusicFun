"""
Main runner script for Netease Music crawler.
All output in English, ASCII only.
"""
import sys
import json
from pathlib import Path
from datetime import datetime
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.platforms.netease.crawler import NeteaseCrawler
from src.core.logger import setup_logger
from config.settings import LOG_DIR


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Netease Music Crawler")
    parser.add_argument("--keyword", "-k", default="mihoyo", help="Search keyword (default: mihoyo)")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max songs to process (default: 10)")
    parser.add_argument("--output", "-o", default=None, help="Output filename (default: auto-generated)")
    parser.add_argument("--comments-per-song", "-c", type=int, default=10, help="Max comments per song (default: 10)")
    parser.add_argument("--mock-only", "-m", action="store_true", help="Use mock comments only")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Setup logger (only once)
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logger(log_level=log_level, log_dir=LOG_DIR)

    logger.info("=" * 50)
    logger.info("Netease Music Crawler Started")
    logger.info(f"Keyword: {args.keyword}")
    logger.info(f"Max songs: {args.limit}")
    logger.info(f"Comments per song: {args.comments_per_song}")
    logger.info(f"Mock only: {args.mock_only}")
    logger.info("=" * 50)

    try:
        # Create crawler instance with mock flag
        crawler = NeteaseCrawler(use_mock=args.mock_only)

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
            output_file = f"netease_{args.keyword}_{timestamp}.json"

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
        total_comments = 0
        for idx, (song_name, data) in enumerate(results.items(), 1):
            comment_count = len(data.get("hot_comments", []))
            total_comments += comment_count
            print(f"{idx}. {song_name[:50]} - {comment_count} comments")
        print("-" * 50)
        print(f"Total songs: {len(results)}")
        print(f"Total comments: {total_comments}")
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